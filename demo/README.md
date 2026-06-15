# Demo: From Requirement to Running Code

This demo shows the complete **Spec-Driven Vibe Coding** workflow:

```
Requirement Document
    ↓
spec-harness generate
    ↓
User Stories + Acceptance Criteria + API Spec + Tasks
    ↓
spec-harness generate-tests
    ↓
pytest Skeletons
    ↓
Implement Code (or feed to AI coding agent)
    ↓
pytest → All Tests Pass
```

## Step 1: Write Requirement

See [`requirements/attachment_management.md`](requirements/attachment_management.md)

## Step 2: Generate Specs

```bash
spec-harness generate requirements/attachment_management.md
```

Generated artifacts in [`specs/`](specs/):
- `user_stories.md` — 6 user stories
- `acceptance_criteria.md` — 24 acceptance criteria
- `api_spec.yaml` — 21 API endpoints
- `test_cases.md` — 41 test cases
- `task_breakdown.yaml` — 24 tasks
- `ai_coding_tasks.md` — 24 AI coding prompts

## Step 3: Generate Test Skeletons

```bash
spec-harness generate-tests specs/api_spec.yaml --output tests
```

Generated [`tests/pytest/`](tests/pytest/) with test stubs.

## Step 4: Implement Code

Based on the API spec and test skeletons, we implemented a FastAPI service:

[`implementation/main.py`](implementation/main.py)

Key features:
- Upload/Preview/Download/Print/Delete/List attachments
- Permission checks (ATTACHMENT_UPLOAD, ATTACHMENT_DELETE, etc.)
- Audit logging for all operations
- RESTful API design matching the spec

## Step 5: Run Tests

```bash
PYTHONPATH=demo/implementation pytest demo/tests/pytest/ -v
```

**Result:** 4 tests passed ✅

```
demo/tests/pytest/test_upload_attachment.py::test_upload_attachment_success PASSED
demo/tests/pytest/test_upload_attachment.py::test_upload_attachment_unauthorized PASSED
demo/tests/pytest/test_upload_attachment.py::test_upload_attachment_forbidden PASSED
demo/tests/pytest/test_upload_attachment.py::test_upload_attachment_validation_error PASSED
```

## What This Proves

- ✅ Raw requirements → structured specs (in seconds)
- ✅ Specs → test skeletons (automatically)
- ✅ Test skeletons → working code (with AI or manual)
- ✅ Tests verify the implementation matches the spec
- ✅ Full traceability: Requirement → Story → API → Test → Code

## Next: Feed AI Coding Tasks to Claude Code

Each task in `specs/ai_coding_tasks.md` includes:
- Context, Goal, Requirements
- Acceptance Criteria
- Testing Requirements
- Files to Modify
- Out of Scope

Copy any task into Claude Code and watch it implement the feature with full context.
