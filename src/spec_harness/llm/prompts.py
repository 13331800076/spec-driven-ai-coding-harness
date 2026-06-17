# ruff: noqa: E501
# ruff: noqa: E501
"""Enhanced LLM prompts for high-quality spec generation."""

from spec_harness.models import DomainAnalysis, RequirementSpec

SYSTEM_PROMPT = """You are a senior software requirements analyst and technical writer with 10 years of experience in enterprise software delivery.

Your expertise:
- Domain-Driven Design (DDD)
- Behavior-Driven Development (BDD)
- Test-Driven Development (TDD)
- API design and RESTful architecture
- Enterprise permission and audit patterns

Rules for all outputs:
1. Be specific and concrete — avoid vague terms like "optimize", "improve", "enhance"
2. Use professional business language, not casual chat
3. Each user story must be independently implementable and testable
4. Acceptance criteria must be objectively verifiable (pass/fail)
5. API specs must include exact field names, types, and validation rules
6. Always consider edge cases: permission failure, invalid data, missing resources, concurrency"""


def requirement_analysis_prompt(spec: RequirementSpec, domain: DomainAnalysis) -> str:
    """Generate prompt for LLM-based requirement analysis refinement."""
    return f"""Given the following requirement and initial domain analysis, refine and improve the structured output.

Requirement Title: {spec.title}

Raw Text:
{spec.raw_text}

Initial Domain Analysis:
- Modules: {domain.modules}
- Business Objects: {domain.business_objects}
- Roles: {domain.roles}
- Operations: {domain.operations}
- Permissions: {domain.permissions}
- Constraints: {domain.constraints}

Your task: Clean up and improve the domain analysis. Remove stop words, normalize roles, deduplicate objects, and ensure all elements are specific and actionable.

Return JSON:
{{
  "modules": [list of specific business modules],
  "business_objects": [list of domain entities, clean, no verbs or stop words],
  "roles": [list of user roles, normalized, singular form],
  "operations": [list of action verbs],
  "permissions": [list of permission identifiers in UPPER_SNAKE_CASE],
  "constraints": [list of concrete business rules with conditions]
}}
"""


def user_stories_prompt(spec: RequirementSpec, domain: DomainAnalysis) -> str:
    """Generate prompt for LLM-based user story generation."""
    return f"""Based on the following requirement, generate high-quality user stories in standard format.

Requirement Title: {spec.title}

Raw Text:
{spec.raw_text}

Domain Context:
- Roles: {domain.roles}
- Business Objects: {domain.business_objects}
- Operations: {domain.operations}

Story Generation Rules:
1. Each story MUST follow exact format: As a [role], I want to [action], so that [value]
2. Each story covers ONE specific action only — split compound actions
3. Role must be a realistic user persona (business user, system admin, procurement manager)
4. Action must be specific and measurable (not "manage" but "upload attachments to purchase orders")
5. Value must explain WHY the business needs this, not just WHAT it does
6. Generate stories for ALL operations mentioned in the requirement
7. Title should be 3-6 words, concise and clear

Return JSON:
{{
  "stories": [
    {{
      "id": "US-001",
      "title": "Upload attachments",
      "role": "business user",
      "action": "upload attachments to business documents",
      "value": "supporting materials can be stored and reviewed later by the team"
    }}
  ]
}}
"""


def acceptance_criteria_prompt(story_json: str) -> str:
    """Generate prompt for LLM-based acceptance criteria generation."""
    return f"""Given the following user story, generate comprehensive acceptance criteria in Given/When/Then format.

User Story:
{story_json}

Acceptance Criteria Rules:
1. Generate EXACTLY 4 acceptance criteria per story:
   - AC-1: Success path (happy path)
   - AC-2: Permission/authentication failure
   - AC-3: Validation/data error
   - AC-4: Audit/logging (if applicable) or edge case
2. Use precise, testable language — each criterion must be pass/fail verifiable
3. Given must set up the exact preconditions (user role, permissions, data state)
4. When must describe the exact action or trigger
5. Then must describe the exact observable outcome
6. Include 1-2 And conditions for additional expectations
7. For permission failures, specify exact permission name and error response

Return JSON:
{{
  "criteria": [
    {{
      "id": "AC-001",
      "given": "Given a business user has ATTACHMENT_UPLOAD permission and a valid PDF file",
      "when": "When the user uploads the file to a purchase order",
      "then": "Then the file is stored successfully and linked to the purchase order",
      "and_conditions": ["And the system returns attachment_id and file_name", "And an audit log is created with user_id and timestamp"]
    }}
  ]
}}
"""


def api_spec_prompt(spec: RequirementSpec, domain: DomainAnalysis, stories_json: str) -> str:
    """Generate prompt for LLM-based API spec generation."""
    return f"""Design REST API endpoints based on the following requirement, domain model, and user stories.

Requirement: {spec.title}

Domain:
- Objects: {domain.business_objects}
- Operations: {domain.operations}
- Permissions: {domain.permissions}

User Stories:
{stories_json}

API Design Rules:
1. Follow RESTful conventions: GET /resources, POST /resources, GET /resources/{id}, DELETE /resources/{id}
2. Use nouns for resources (attachments, not uploadAttachment)
3. Include permission_required for ALL mutating operations (POST, PUT, DELETE)
4. Define request schema with exact field names, types (string, integer, boolean, binary, object, list), and required/optional
5. Define response schema with exact field names and types
6. Include standard error codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error)
7. Use consistent naming: snake_case for fields, kebab-case for paths
8. Group related endpoints (e.g., /api/attachments/{id}/preview, /api/attachments/{id}/download)

Return JSON:
{{
  "apis": [
    {{
      "name": "upload_attachment",
      "method": "POST",
      "path": "/api/attachments",
      "permission_required": "ATTACHMENT_UPLOAD",
      "request_schema": {{
        "business_object_type": "string (required)",
        "business_object_id": "string (required)",
        "file": "binary (required)"
      }},
      "response_schema": {{
        "attachment_id": "string",
        "file_name": "string",
        "status": "string"
      }},
      "error_codes": ["400", "401", "403", "500"]
    }}
  ]
}}
"""


def ai_coding_task_prompt(task_json: str) -> str:
    """Generate prompt for LLM-based AI coding task refinement."""
    return f"""Convert the following development task into a detailed, ready-to-use AI coding task.

Task:
{task_json}

AI Coding Task Requirements:
1. Context: Provide 2-3 sentences of business and technical background
2. Goal: One specific, measurable sentence describing what must be achieved
3. Requirements: 3-5 bullet points, each specific and actionable (no vague terms)
4. Acceptance Criteria: 3-5 bullet points, each pass/fail verifiable
5. Testing Requirements: 2-4 bullet points specifying what tests to write
6. Agent Instructions: 3-5 rules (do's and don'ts)
7. Files to Modify: Exact file paths the AI should create or modify
8. Out of Scope: 2-3 explicit exclusions to prevent scope creep

Language Rules:
- NEVER use: optimize, improve, refactor, enhance, clean up, better, nicer, good
- ALWAYS use: implement, add, create, validate, verify, ensure, return, reject, store, link
- Be specific about data types, response formats, and error messages

Return JSON:
{{
  "id": "TASK-001",
  "title": "Implement upload attachment API",
  "context": "The attachment management system needs a REST API for uploading files linked to business documents. This is part of the unified attachment management feature across procurement, sales, and inventory modules.",
  "goal": "Implement a POST /api/attachments endpoint that accepts file uploads, validates permissions, stores files, and creates audit logs.",
  "requirements": [
    "Validate that the user has ATTACHMENT_UPLOAD permission before processing",
    "Accept business_object_type and business_object_id as required form fields",
    "Validate file type (allow PDF, PNG, JPG, DOCX, XLSX only) and reject invalid types",
    "Store file metadata in database (file_name, file_size, mime_type, storage_path)",
    "Create an audit log entry with user_id, timestamp, action='UPLOAD', and attachment_id"
  ],
  "acceptance_criteria": [
    "Upload succeeds for authorized users and returns attachment_id and file_name",
    "Invalid file type returns 400 Bad Request with clear error message",
    "Missing business_object_id returns 400 Bad Request",
    "Unauthorized users receive 403 Forbidden with permission denied message",
    "Audit log is created with correct user_id, timestamp, and action='UPLOAD'"
  ],
  "testing_requirements": [
    "Add pytest test for successful upload with valid PDF file",
    "Add pytest test for invalid file type rejection (400)",
    "Add pytest test for missing permission (403)",
    "Add pytest test for audit log creation after successful upload"
  ],
  "agent_instructions": [
    "Do not modify unrelated modules (user management, authentication, frontend)",
    "Add tests before or alongside implementation",
    "Keep API response format consistent with api_spec.yaml",
    "Use dependency injection for storage service so it can be mocked in tests",
    "Ensure file cleanup in test teardown to avoid disk pollution"
  ],
  "files_to_modify": [
    "src/routers/attachments.py",
    "src/services/attachment_service.py",
    "src/models/attachment.py",
    "src/schemas/attachment.py",
    "tests/test_upload_attachment.py"
  ],
  "out_of_scope": [
    "Frontend upload UI",
    "Cloud storage integration (use local filesystem for now)",
    "File virus scanning",
    "Image thumbnail generation"
  ]
}}
"""
