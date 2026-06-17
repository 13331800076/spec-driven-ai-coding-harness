"""CLI entry point for spec-driven-ai-coding-harness."""

from pathlib import Path

import typer
from rich.console import Console

from spec_harness.analyzer.domain_analyzer import DomainAnalyzer
from spec_harness.config import HarnessConfig
from spec_harness.generators.acceptance_generator import AcceptanceCriteriaGenerator
from spec_harness.generators.agent_task_generator import AgentTaskGenerator
from spec_harness.generators.api_spec_generator import ApiSpecGenerator
from spec_harness.generators.task_breakdown_generator import TaskBreakdownGenerator
from spec_harness.generators.test_case_generator import TestCaseGenerator
from spec_harness.generators.user_story_generator import UserStoryGenerator
from spec_harness.parser.requirement_parser import RequirementParser
from spec_harness.renderers.markdown_renderer import MarkdownRenderer, YamlRenderer
from spec_harness.testgen.pytest_generator import PytestGenerator

app = typer.Typer(help="Spec-Driven AI Coding Harness")
console = Console()


@app.command()
def init(
    project_name: str = typer.Option("my-project", "--name", "-n", help="Project name"),
    output_dir: str = typer.Option("outputs", "--output", "-o", help="Output directory"),
):
    """Initialize a new harness project."""
    cwd = Path.cwd()
    (cwd / "requirements").mkdir(exist_ok=True)
    (cwd / output_dir).mkdir(exist_ok=True)
    (cwd / "templates").mkdir(exist_ok=True)

    harness_yaml = cwd / "harness.yaml"
    if not harness_yaml.exists():
        harness_yaml.write_text(
            f"""project:
  name: {project_name}
  output_dir: {output_dir}

generation:
  mode: rule_based
  language: en
  output_formats:
    - markdown
    - yaml

llm:
  provider: openai_compatible
  model: gpt-4.1
  base_url: ${{OPENAI_BASE_URL}}
  api_key: ${{OPENAI_API_KEY}}

testing:
  generate_pytest: true
  generate_playwright: true

quality_gates:
  require_acceptance_criteria: true
  require_test_cases: true
  require_task_traceability: true
""",
            encoding="utf-8",
        )
        console.print("[green]Created harness.yaml[/green]")

    console.print(f"[green]Initialized project '{project_name}'[/green]")
    console.print("  requirements/  - Place requirement .md files here")
    console.print(f"  {output_dir}/    - Generated artifacts will appear here")


@app.command()
def generate(
    requirement_file: str = typer.Argument(..., help="Path to requirement markdown file"),
    config_path: str = typer.Option(
        "harness.yaml", "--config", "-c", help="Path to harness config"
    ),
):
    """Generate specifications from a requirement document."""
    config = HarnessConfig.load(config_path)
    output_dir = config.get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    md_renderer = MarkdownRenderer(templates_dir)
    yaml_renderer = YamlRenderer()

    # LLM orchestrator (if enabled)
    llm_orchestrator = None
    if config.generation.mode == "llm":
        from spec_harness.llm.orchestrator import LLMOrchestrator

        llm_orchestrator = LLMOrchestrator(config)
        if not llm_orchestrator.client.is_available():
            console.print(
                "[yellow]Warning: LLM mode configured but API key not available. "
                "Falling back to rule-based mode.[/yellow]"
            )
            llm_orchestrator = None

    # Parse requirement
    parser = RequirementParser()
    spec = parser.parse(requirement_file)
    console.print(f"[blue]Parsed requirement:[/blue] {spec.title}")

    # Analyze domain
    analyzer = DomainAnalyzer()
    domain = analyzer.analyze(spec)
    console.print(
        f"[blue]Domain analysis:[/blue] {len(domain.operations)} ops, "
        f"{len(domain.business_objects)} objects"
    )

    # Optionally refine with LLM
    if llm_orchestrator:
        console.print("[blue]Refining domain with LLM...[/blue]")
        domain = llm_orchestrator.refine_domain(spec, domain)

    # Generate user stories
    if llm_orchestrator:
        console.print("[blue]Generating stories with LLM...[/blue]")
        llm_stories = llm_orchestrator.generate_stories(spec, domain)
        if llm_stories:
            stories = llm_stories
        else:
            us_gen = UserStoryGenerator()
            stories = us_gen.generate(spec, domain)
    else:
        us_gen = UserStoryGenerator()
        stories = us_gen.generate(spec, domain)
    md_renderer.render_to_file(
        "user_story.md.j2",
        {"stories": [s.model_dump() for s in stories]},
        output_dir / "user_stories.md",
    )
    console.print(f"[green]Generated {len(stories)} user stories[/green]")

    # Generate acceptance criteria
    if llm_orchestrator:
        console.print("[blue]Generating acceptance criteria with LLM...[/blue]")
        llm_ac = llm_orchestrator.generate_acceptance_criteria(stories)
        if llm_ac:
            ac_groups = llm_ac
        else:
            ac_gen = AcceptanceCriteriaGenerator()
            ac_groups = ac_gen.generate(stories)
    else:
        ac_gen = AcceptanceCriteriaGenerator()
        ac_groups = ac_gen.generate(stories)
    md_renderer.render_to_file(
        "acceptance_criteria.md.j2",
        {
            "acceptance_criteria_groups": [
                {
                    "story_id": g.story_id,
                    "story_title": g.story_title,
                    "criteria": [c.model_dump() for c in g.criteria],
                }
                for g in ac_groups
            ]
        },
        output_dir / "acceptance_criteria.md",
    )
    console.print("[green]Generated acceptance criteria[/green]")

    # Generate domain model YAML
    yaml_renderer.render(
        {"domain": domain.model_dump()},
        output_dir / "domain_model.yaml",
    )
    console.print("[green]Generated domain_model.yaml[/green]")

    # Generate API specs
    if llm_orchestrator:
        console.print("[blue]Generating API specs with LLM...[/blue]")
        llm_apis = llm_orchestrator.generate_api_specs(spec, domain, stories)
        if llm_apis:
            apis = llm_apis
        else:
            api_gen = ApiSpecGenerator()
            apis = api_gen.generate(spec, domain, stories)
    else:
        api_gen = ApiSpecGenerator()
        apis = api_gen.generate(spec, domain, stories)
    md_renderer.render_to_file(
        "api_spec.yaml.j2",
        {"apis": [a.model_dump() for a in apis]},
        output_dir / "api_spec.yaml",
    )
    console.print(f"[green]Generated {len(apis)} API specs[/green]")

    # Generate test cases
    tc_gen = TestCaseGenerator()
    test_cases = tc_gen.generate(ac_groups, apis)
    md_renderer.render_to_file(
        "test_case.md.j2",
        {"test_cases": [t.model_dump() for t in test_cases]},
        output_dir / "test_cases.md",
    )
    console.print(f"[green]Generated {len(test_cases)} test cases[/green]")

    # Generate task breakdown
    task_gen = TaskBreakdownGenerator()
    tasks = task_gen.generate(stories, ac_groups, apis, test_cases)
    md_renderer.render_to_file(
        "task_breakdown.yaml.j2",
        {"tasks": [t.model_dump() for t in tasks]},
        output_dir / "task_breakdown.yaml",
    )
    console.print(f"[green]Generated {len(tasks)} tasks[/green]")

    # Generate AI coding tasks
    agent_gen = AgentTaskGenerator()
    ai_tasks = agent_gen.generate(tasks)
    md_renderer.render_to_file(
        "ai_coding_task.md.j2",
        {"tasks": [t.model_dump() for t in ai_tasks]},
        output_dir / "ai_coding_tasks.md",
    )
    console.print(f"[green]Generated {len(ai_tasks)} AI coding tasks[/green]")

    console.print(f"[bold green]All artifacts written to {output_dir}/[/bold green]")


@app.command()
def validate(
    outputs_dir: str = typer.Argument(..., help="Path to outputs directory"),
    config_path: str = typer.Option(
        "harness.yaml", "--config", "-c", help="Path to harness config"
    ),
):
    """Validate generated specifications."""
    _config = HarnessConfig.load(config_path)
    output_dir = Path(outputs_dir)

    if not output_dir.exists():
        console.print(f"[red]Directory not found: {outputs_dir}[/red]")
        raise typer.Exit(code=1)

    # TODO: Load generated artifacts and validate
    # For MVP, we do a simple file existence check
    required_files = [
        "user_stories.md",
        "acceptance_criteria.md",
        "api_spec.yaml",
        "test_cases.md",
        "task_breakdown.yaml",
    ]

    missing = [f for f in required_files if not (output_dir / f).exists()]
    if missing:
        console.print(f"[red]Missing required files: {', '.join(missing)}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]Validation passed: all required artifacts present.[/green]")


@app.command()
def generate_tests(
    api_spec_file: str = typer.Argument(..., help="Path to api_spec.yaml"),
    output_dir: str = typer.Option("outputs/tests", "--output", "-o", help="Test output directory"),
):
    """Generate pytest and Playwright skeletons from API specs."""
    import yaml

    spec_path = Path(api_spec_file)
    if not spec_path.exists():
        console.print(f"[red]API spec file not found: {api_spec_file}[/red]")
        raise typer.Exit(code=1)

    with open(spec_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    from spec_harness.models import ApiSpec

    apis = [ApiSpec(**api) for api in data.get("apis", [])]

    test_out = Path(output_dir)
    test_out.mkdir(parents=True, exist_ok=True)

    # Generate pytest skeletons
    pytest_gen = PytestGenerator()
    pytest_gen.generate(apis, test_out)
    console.print(f"[green]Generated pytest skeletons in {test_out}/pytest/[/green]")

    console.print("[bold green]Test skeletons generated.[/bold green]")


@app.command()
def export_agent_tasks(
    task_breakdown_file: str = typer.Argument(..., help="Path to task_breakdown.yaml"),
    output_dir: str = typer.Option(
        "outputs/agent_tasks", "--output", "-o", help="Agent task output directory"
    ),
):
    """Export individual AI coding task files from task breakdown."""
    import yaml

    task_path = Path(task_breakdown_file)
    if not task_path.exists():
        console.print(f"[red]Task breakdown file not found: {task_breakdown_file}[/red]")
        raise typer.Exit(code=1)

    with open(task_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    agent_out = Path(output_dir)
    agent_out.mkdir(parents=True, exist_ok=True)

    # Write placeholder agent task files
    for task in data.get("tasks", []):
        task_id = task.get("id", "TASK-000")
        task_file = agent_out / f"{task_id}.md"
        task_file.write_text(
            f"""# {task_id}: {task.get('title', 'Untitled')}

## Context
This task is part of the feature implementation.

## Goal
{task.get('title', 'Implement the feature')}

## Acceptance Criteria
{chr(10).join(f"- {ac}" for ac in task.get('acceptance_criteria', []))}

## Files to Modify
{chr(10).join(f"- {f}" for f in task.get('files_to_modify', []))}

## Out of Scope
{chr(10).join(f"- {item}" for item in task.get('out_of_scope', []))}

## Instructions for AI Coding Agent
- Do not modify unrelated modules.
- Add tests before implementation.
- Keep API response format consistent with api_spec.yaml.
""",
            encoding="utf-8",
        )

    console.print(
        f"[green]Exported {len(data.get('tasks', []))} agent tasks to {agent_out}/[/green]"
    )


def main():
    app()


if __name__ == "__main__":
    main()
