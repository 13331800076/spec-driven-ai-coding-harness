"""LLM orchestrator for spec generation."""

from spec_harness.config import HarnessConfig
from spec_harness.llm import prompts
from spec_harness.llm.client import LLMClient
from spec_harness.models import (
    AcceptanceCriteriaGroup,
    AcceptanceCriterion,
    AiCodingTask,
    ApiSpec,
    DomainAnalysis,
    RequirementSpec,
    Task,
    UserStory,
)


class LLMOrchestrator:
    """Orchestrate LLM-based spec generation."""

    def __init__(self, config: HarnessConfig):
        self.client = LLMClient(config)

    def refine_domain(self, spec: RequirementSpec, domain: DomainAnalysis) -> DomainAnalysis:
        if not self.client.is_available():
            return domain
        prompt = prompts.requirement_analysis_prompt(spec, domain)
        try:
            result = self.client.generate_json(prompt)
            return DomainAnalysis(**result)
        except Exception as e:
            print(f"[LLM warning] Domain refinement failed: {e}. Using rule-based output.")
            return domain

    def generate_stories(self, spec: RequirementSpec, domain: DomainAnalysis) -> list[UserStory]:
        if not self.client.is_available():
            return []
        prompt = prompts.user_stories_prompt(spec, domain)
        try:
            result = self.client.generate_json(prompt)
            stories = []
            for s in result.get("stories", []):
                stories.append(UserStory(**s))
            return stories
        except Exception as e:
            print(f"[LLM warning] Story generation failed: {e}. Using rule-based output.")
            return []

    def generate_acceptance_criteria(
        self, stories: list[UserStory]
    ) -> list[AcceptanceCriteriaGroup]:
        if not self.client.is_available():
            return []
        groups = []
        for story in stories:
            story_json = story.model_dump_json()
            prompt = prompts.acceptance_criteria_prompt(story_json)
            try:
                result = self.client.generate_json(prompt)
                criteria = [AcceptanceCriterion(**c) for c in result.get("criteria", [])]
                groups.append(
                    AcceptanceCriteriaGroup(
                        story_id=story.id,
                        story_title=story.title,
                        criteria=criteria,
                    )
                )
            except Exception as e:
                print(
                    f"[LLM warning] AC generation for {story.id} "
                    f"failed: {e}. Using rule-based output."
                )
                return []
        return groups

    def generate_api_specs(
        self, spec: RequirementSpec, domain: DomainAnalysis, stories: list[UserStory]
    ) -> list[ApiSpec]:
        if not self.client.is_available():
            return []
        stories_json = "\n".join([s.model_dump_json() for s in stories[:5]])
        prompt = prompts.api_spec_prompt(spec, domain, stories_json)
        try:
            result = self.client.generate_json(prompt)
            return [ApiSpec(**a) for a in result.get("apis", [])]
        except Exception as e:
            print(f"[LLM warning] API spec generation failed: {e}. Using rule-based output.")
            return []

    def refine_ai_tasks(self, tasks: list[Task]) -> list[AiCodingTask]:
        if not self.client.is_available():
            return []
        ai_tasks = []
        for task in tasks:
            task_json = task.model_dump_json()
            prompt = prompts.ai_coding_task_prompt(task_json)
            try:
                result = self.client.generate_json(prompt)
                ai_tasks.append(AiCodingTask(**result))
            except Exception as e:
                print(
                    f"[LLM warning] AI task refinement for {task.id} "
                    f"failed: {e}. Using rule-based output."
                )
                return []
        return ai_tasks
