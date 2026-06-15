# Vibe Coding Workflow

## What is Vibe Coding?

Vibe Coding is the practice of using AI coding assistants (Claude Code, Codex, Cursor, Cline) to write software. The "vibe" refers to the conversational, iterative nature of the process.

## The Problem with Unstructured Vibe Coding

```
Requirement (vague)
    ↓
AI writes code
    ↓
Does it work? Maybe.
    ↓
Fix bugs iteratively
    ↓
Ship something that "sort of" works
```

Problems:
- Requirements are not clarified before coding
- No acceptance criteria to judge correctness
- No tests to validate behavior
- Code is often "one-shot" and not maintainable
- Difficult to reproduce or scale across team members

## Spec-Driven Vibe Coding

```
Requirement Document
    ↓
Requirement Parser (clarifies the requirement)
    ↓
User Stories (defines who, what, why)
    ↓
Acceptance Criteria (defines when it's done)
    ↓
API Spec (defines the contract)
    ↓
Test Cases (defines how to verify)
    ↓
Task Breakdown (defines what to build)
    ↓
AI Coding Tasks (structured prompts for AI)
    ↓
pytest / Playwright Skeletons (test scaffolding)
    ↓
AI implements with tests (Test-First AI Coding)
    ↓
Validation (Quality Gates check completeness)
    ↓
Deliver with confidence
```

## Why This Works

1. **Requirements are clarified** before any code is written
2. **Acceptance criteria** provide objective measures of "done"
3. **Tests exist first** - AI can write code to make tests pass
4. **Tasks are scoped** - each AI coding task is small and focused
5. **Traceability** - every line of code can be traced back to a requirement
6. **Reproducibility** - same inputs produce same outputs, regardless of who is prompting

## Using This Harness for Vibe Coding

### Step 1: Write a Requirement Document

```markdown
# Requirement: Feature X

Users should be able to...
The system should support...
```

### Step 2: Generate Specifications

```bash
spec-harness generate requirements/feature_x.md
```

### Step 3: Review Generated Artifacts

Open `outputs/user_stories.md`, `outputs/acceptance_criteria.md`, etc. Review and refine.

### Step 4: Validate

```bash
spec-harness validate outputs/
```

### Step 5: Generate Test Skeletons

```bash
spec-harness generate-tests outputs/api_spec.yaml
```

### Step 6: Export AI Coding Tasks

```bash
spec-harness export-agent-tasks outputs/task_breakdown.yaml
```

### Step 7: Feed Tasks to AI Coding Agent

Copy each `outputs/agent_tasks/TASK-001.md` into Claude Code / Codex and let AI implement it.

### Step 8: Run Tests

```bash
pytest outputs/tests/pytest/
```

### Step 9: Validate Again

```bash
spec-harness validate outputs/
```

## Best Practices

- Always review generated specs before giving them to AI
- Never skip the acceptance criteria step
- Add tests before implementation (TDD for AI Coding)
- Keep AI coding tasks small (1-3 files per task)
- Always define out-of-scope for each task
- Use validation as a pre-commit check
