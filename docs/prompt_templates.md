# Prompt Templates

This document contains the prompt templates used by the harness for LLM mode. In rule-based mode, these prompts are not used; instead, heuristic templates generate the outputs.

## Requirement Parser Prompt (LLM Mode)

```
You are a requirements analyst. Parse the following requirement document and extract structured information.

Requirement Document:
{requirement_text}

Extract and return JSON with these fields:
- title: The main requirement title
- background: Context and motivation
- actors: List of user roles mentioned
- business_objects: List of business entities/objects
- features: List of functional features (what users should be able to do)
- constraints: List of constraints, permissions, audit requirements, validation rules

Return only valid JSON.
```

## User Story Generator Prompt (LLM Mode)

```
You are a product manager. Given the following requirement and domain analysis, generate user stories in standard format.

Requirement: {requirement_title}
Domain Analysis: {domain_analysis}
Features: {features}

For each feature, generate one user story with:
- id: US-001, US-002, etc.
- title: Short title
- role: The user role
- action: What they want to do
- value: The business value

Format each story as:
As a [role],
I want to [action],
so that [value].

Return as JSON array.
```

## Acceptance Criteria Generator Prompt (LLM Mode)

```
You are a QA engineer. For each user story, generate acceptance criteria in Given/When/Then format.

User Story: {user_story}

Generate at least 3 acceptance criteria per story:
1. Success path (happy path)
2. Permission/authentication failure
3. Validation/error case
4. Audit/logging (if applicable)

Format:
Given [context]
When [action]
Then [expected result]
And [additional condition]

Return as JSON array with fields: id, given, when, then, and_conditions.
```

## API Spec Generator Prompt (LLM Mode)

```
You are a backend architect. Given the domain analysis and user stories, design REST API endpoints.

Domain: {domain_analysis}
Stories: {user_stories}

For each operation, generate:
- name: operation_name
- method: HTTP method
- path: URL path
- permission_required: Permission identifier
- request_schema: Request fields and types
- response_schema: Response fields and types
- error_codes: List of possible HTTP error codes

Return as JSON array.
```

## AI Coding Task Prompt (LLM Mode)

```
You are an AI coding task designer. Given the following development task, create a detailed prompt for an AI coding agent.

Task: {task}
Context: {project_context}

Create a prompt that includes:
1. Context - Business/technical background
2. Goal - What the AI should achieve
3. Requirements - Specific implementation requirements
4. Acceptance Criteria - How to verify completion
5. Testing Requirements - What tests to add
6. Agent Instructions - Rules for the AI (don't modify unrelated files, add tests first, etc.)
7. Files to Modify - Specific files
8. Out of Scope - What NOT to do

Return as structured JSON.
```

## Rule-Based vs LLM Mode

| Aspect | Rule-Based | LLM Mode |
|--------|-----------|----------|
| API Key | Not required | Required |
| Cost | Free | Per-token cost |
| Quality | Structured, predictable | More natural, contextual |
| Speed | Fast | Network latency |
| Use Case | CI/CD, automated pipelines | Initial generation, refinement |

## Switching Modes

In `harness.yaml`:

```yaml
generation:
  mode: rule_based  # or llm
```
