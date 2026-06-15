# Spec-Driven AI Coding Harness

> Turn vague requirements into structured specs, tests, and AI-ready tasks — in seconds.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-35%2F35%20passing-brightgreen)](tests/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**A lightweight CLI that transforms raw requirement documents into user stories, acceptance criteria, API specs, test cases, and AI coding tasks.**

No more "vibe coding" into the void. Give your AI coding agent (Claude Code, Codex, Cursor, Cline) structured context, clear boundaries, and testable specs — so it writes the right code the first time.

---

## Why this matters

Most AI coding failures aren't because the model can't write code. They happen because:

- ❌ Requirements are vague and ambiguous
- ❌ No user stories = no clear scope
- ❌ No acceptance criteria = no way to verify correctness
- ❌ No tests = "looks like it works" code that breaks later
- ❌ Tasks are too big = AI modifies 20 files at once and breaks everything

**This harness fixes that.** It sits between your raw requirements and your AI coding agent, turning chaos into structured, traceable, testable engineering artifacts.

---

## What it generates

| Artifact | Description | Format |
|----------|-------------|--------|
| **User Stories** | As a [role], I want to [action]... | Markdown |
| **Acceptance Criteria** | Given/When/Then criteria per story | Markdown |
| **Domain Model** | Business objects, roles, permissions | YAML |
| **API Specs** | REST endpoints with schemas | YAML |
| **Test Cases** | Steps + expected results | Markdown |
| **Task Breakdown** | Development tasks with traceability | YAML |
| **AI Coding Tasks** | Ready-to-paste prompts for Claude/Codex | Markdown |
| **pytest Skeleton** | Python test stubs | pytest |
| **Playwright Skeleton** | E2E test stubs | Playwright |

---

## 🎬 Demo: From Requirement to AI-Ready Tasks in 30 Seconds

See the full terminal workflow in [`docs/assets/terminal-demo.md`](docs/assets/terminal-demo.md):

```bash
$ spec-harness generate examples/requirements/attachment_management.md

Parsed requirement: Requirement: Unified Attachment Management
Domain analysis: 7 ops, 12 objects
Generated 6 user stories
Generated acceptance criteria
Generated 21 API specs
Generated 41 test cases
Generated 24 tasks
Generated 24 AI coding tasks
All artifacts written to outputs/
```

**Full workflow:** Write requirement → Generate specs → Validate → Export AI tasks → Feed to Claude Code

---

## Quick Start

> 📺 See the full workflow in action: [`docs/assets/terminal-demo.md`](docs/assets/terminal-demo.md)

### Installation

```bash
git clone https://github.com/yourusername/spec-driven-ai-coding-harness.git
cd spec-driven-ai-coding-harness
pip install -e ".[dev]"
```

### 1. Initialize a project

```bash
spec-harness init --name my-project
```

### 2. Write a requirement document

```markdown
# Requirement: Unified Attachment Management

The system should provide a unified attachment management feature across procurement, sales, and inventory modules.

Users should be able to upload, preview, download, print, and delete attachments.

The system should support permission control. Only users with proper permissions can delete or print attachments.

The system should record audit logs for each attachment operation.

The attachment service should expose APIs for upload, download, preview, delete, and list operations.
```

Save to `requirements/attachment_management.md`.

### 3. Generate all specs

```bash
spec-harness generate requirements/attachment_management.md
```

**Output:**
```
✓ Generated 6 user stories
✓ Generated acceptance criteria
✓ Generated domain_model.yaml
✓ Generated 6 API specs
✓ Generated 24 test cases
✓ Generated 6 tasks
✓ Generated 6 AI coding tasks
✓ All artifacts written to outputs/
```

### 4. Review the generated artifacts

```bash
cat outputs/user_stories.md
```

```markdown
# User Stories

## US-001: Upload attachments

As a business user,
I want to upload attachments to business documents,
so that supporting materials can be stored and reviewed later.

## US-002: Preview attachments

As a user,
I want to preview uploaded attachments,
so that I can verify file content without downloading it.
```

### 5. Validate traceability

```bash
spec-harness validate outputs/
```

```
✓ Validation passed: all required artifacts present.
```

### 6. Export AI coding tasks

```bash
spec-harness export-agent-tasks outputs/task_breakdown.yaml
```

Now copy any `outputs/agent_tasks/TASK-001.md` into Claude Code and let it implement the task with full context, scope, and acceptance criteria.

---

## Two generation modes

### Rule-Based Mode (default, no API key needed)

Uses heuristics and templates to generate structured specs from your requirements. Works entirely offline, fast, and deterministic.

```yaml
# harness.yaml
generation:
  mode: rule_based
```

### LLM Mode (OpenAI-compatible, higher quality)

Uses LLM prompts to generate more natural, higher-quality specs. Requires an API key.

```yaml
# harness.yaml
generation:
  mode: llm

llm:
  provider: openai_compatible
  model: gpt-4.1
  base_url: ${{OPENAI_BASE_URL}}
  api_key: ${{OPENAI_API_KEY}}
```

```bash
export OPENAI_API_KEY=sk-...
spec-harness generate requirements/feature.md
```

The LLM refines domain analysis, writes better user stories, generates more precise acceptance criteria, and designs cleaner API specs. Falls back to rule-based if the LLM call fails.

---

## Example: Full pipeline from requirement to AI task

```bash
# 1. Write requirement
spec-harness init

# 2. Generate all artifacts
spec-harness generate requirements/attachment_management.md

# 3. Validate everything is connected
spec-harness validate outputs/

# 4. Generate test skeletons
spec-harness generate-tests outputs/api_spec.yaml

# 5. Export AI-ready task prompts
spec-harness export-agent-tasks outputs/task_breakdown.yaml

# 6. Give TASK-001.md to Claude Code
# 7. Run tests
pytest outputs/tests/pytest/
```

---

## Quality Gates

Not just generation — validation too:

- **Traceability Check**: Requirement → Story → AC → Test → Task → AI Task
- **Completeness Check**: Missing roles, objects, permissions, error scenarios
- **AI Safety Check**: Tasks too large? Missing tests? Vague descriptions? Missing out-of-scope?

---

## Architecture

```
Raw Requirement (.md)
    ↓
Requirement Parser  →  RequirementSpec
    ↓
Domain Analyzer     →  DomainAnalysis
    ↓
Spec Generators     →  UserStories / AcceptanceCriteria / APISpecs / TestCases
    ↓
Task Generators     →  Tasks / AI Coding Tasks
    ↓
Test Generators     →  pytest / Playwright Skeletons
    ↓
Validators          →  Traceability + Quality Gate Report
    ↓
Markdown / YAML / pytest / Playwright Output
```

---

## Tech Stack

- **Python 3.11+** — Modern type hints, Pydantic v2
- **Typer** — Rich CLI with colors and progress
- **Jinja2** — Template-based output rendering
- **pytest** — Test skeleton generation
- **Playwright** — E2E test skeleton generation
- **httpx** — LLM API client (OpenAI-compatible)

---

## What this project demonstrates

Built for **AI Application Engineer**, **Developer Productivity Engineer**, **AI Coding Engineer** roles:

- ✅ Understanding of AI Coding engineering challenges (vague requirements, missing acceptance criteria, no test scaffolding)
- ✅ Ability to design structured AI Coding workflows (not just "chat and hope")
- ✅ Bridging product requirements → structured engineering assets → AI coding tasks
- ✅ DDD, BDD, TDD, SDD concepts applied to AI-assisted delivery
- ✅ Quality gate and traceability thinking for enterprise software delivery

---

## Roadmap

- [x] **v1.0** CLI + file output, rule-based generation, pytest/Playwright skeletons, traceability validation
- [ ] **v1.1** LLM mode with OpenAI-compatible API for higher-quality natural-language specs
- [ ] **v1.2** FastAPI web UI for visualization and collaborative review
- [ ] **v2.0** Direct Codex/Claude Code integration — export and run tasks automatically

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for the Vibe Coding engineering community.**

*If this project helps your AI coding workflow, please ⭐ star it on GitHub!*
