# Terminal Demo: Spec-Driven Vibe Coding Workflow

```bash
$ # Step 1: Initialize a project
$ spec-harness init --name my-erp

Initialized project 'my-erp'
  requirements/  - Place requirement .md files here
  outputs/    - Generated artifacts will appear here

$ # Step 2: Generate specs from a requirement document
$ spec-harness generate examples/requirements/attachment_management.md

Parsed requirement: Requirement: Unified Attachment Management
Domain analysis: 7 ops, 12 objects
Generated 6 user stories
Generated acceptance criteria
Generated domain_model.yaml
Generated 21 API specs
Generated 41 test cases
Generated 24 tasks
Generated 24 AI coding tasks
All artifacts written to outputs/

$ # Step 3: Review generated user stories
$ cat outputs/user_stories.md

# User Stories

## US-001: Upload attachments

As a business user,
I want to upload attachments to business documents,
so that supporting materials can be stored and reviewed later.

## US-002: Preview attachments

As a user,
I want to preview uploaded attachments,
so that I can verify file content without downloading it.

$ # Step 4: Generate test skeletons
$ spec-harness generate-tests outputs/api_spec.yaml

Generated pytest skeletons in outputs/tests/pytest/
Test skeletons generated.

$ # Step 5: Validate traceability
$ spec-harness validate outputs/

Validation passed: all required artifacts present.

$ # Step 6: Export AI coding tasks
$ spec-harness export-agent-tasks outputs/task_breakdown.yaml

Exported 6 agent tasks to outputs/agent_tasks/

$ # Step 7: Feed AI coding task to Claude Code
$ cat outputs/agent_tasks/TASK-002.md

# TASK-002: Implement upload attachment API

Context:
The system needs a unified attachment upload API for multiple ERP modules.

Goal:
Implement a POST /api/attachments endpoint.

Requirements:
- Validate business_object_type and business_object_id.
- Save uploaded file metadata.
- Return attachment_id, file_name, and status.
- Create audit log after successful upload.

Acceptance Criteria:
- Upload succeeds for authorized users.
- Invalid file type is rejected.
- Audit log is created.

Testing:
- Add pytest cases for successful upload.
- Add pytest cases for invalid file type.
- Add pytest cases for missing permission.

Instructions for AI Coding Agent:
- Do not modify unrelated modules.
- Add tests before implementation.
- Keep API response format consistent with api_spec.yaml.

$ # Full workflow: vague requirement → structured specs → AI-ready tasks
$ # in under 30 seconds. That's Spec-Driven Vibe Coding.
```
