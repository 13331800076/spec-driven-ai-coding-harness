# Design Principles

## 1. Spec-Driven Development (SDD)

Never let AI write code from vague requirements. Always generate structured specifications first:

- Requirement → User Story → Acceptance Criteria → API Spec → Test Cases → Tasks → Code

## 2. Rule-Based First, LLM Optional

The MVP operates entirely in rule-based mode without requiring API keys. LLM mode is available for more natural language generation but is not required for core functionality.

## 3. Traceability by Design

Every artifact must be traceable to its source:

- Requirement → User Story (via requirement_id)
- User Story → Acceptance Criteria (via story_id)
- Acceptance Criteria → Test Cases (via related_ac)
- User Story → Tasks (via related_user_story)
- Task → AI Coding Task (via task_id)

## 4. Quality Gates

Generated artifacts are validated before being considered complete:

- Traceability Check: Ensures no orphaned requirements
- Completeness Check: Ensures no missing roles, permissions, error scenarios
- AI Coding Safety Check: Ensures tasks are specific, scoped, and testable

## 5. Vibe Coding Engineering

The project itself demonstrates the Vibe Coding workflow:

1. Write SPEC.md
2. Break into User Stories
3. Define Acceptance Criteria
4. Generate Tasks
5. Implement with AI assistance
6. Test and validate
7. Review and refine

## 6. Output over Platform

Focus on generating high-quality output artifacts rather than building a complex web platform. The CLI produces files that can be committed to git, reviewed in PRs, and fed to AI coding agents.

## 7. Enterprise Readiness

Design for enterprise software delivery patterns:

- Audit logging considerations
- Permission control patterns
- Multi-module ERP-style features
- Structured test generation
- Task delegation and approval workflows
