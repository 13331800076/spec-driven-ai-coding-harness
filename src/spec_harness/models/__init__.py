"""Core data models for the spec-driven harness."""

from typing import Any

from pydantic import BaseModel, Field


class RequirementSpec(BaseModel):
    """Structured representation of a raw requirement document."""

    requirement_id: str = Field(default="", description="Unique identifier for the requirement")
    title: str = Field(default="", description="Requirement title")
    background: str | None = Field(default=None, description="Background context")
    actors: list[str] = Field(default_factory=list, description="User roles/actors mentioned")
    business_objects: list[str] = Field(
        default_factory=list, description="Business entities/objects"
    )
    features: list[str] = Field(default_factory=list, description="Functional features")
    constraints: list[str] = Field(
        default_factory=list, description="Constraints, permissions, audit requirements"
    )
    raw_text: str = Field(default="", description="Original raw text of the requirement")


class DomainAnalysis(BaseModel):
    """Domain analysis extracted from a requirement specification."""

    modules: list[str] = Field(default_factory=list, description="Business modules identified")
    business_objects: list[str] = Field(default_factory=list, description="Business entities")
    roles: list[str] = Field(default_factory=list, description="User roles")
    permissions: list[str] = Field(default_factory=list, description="Permission identifiers")
    operations: list[str] = Field(default_factory=list, description="Operations/actions identified")
    constraints: list[str] = Field(default_factory=list, description="Constraints and rules")


class UserStory(BaseModel):
    """Standard user story format."""

    id: str = Field(default="", description="Unique story ID, e.g., US-001")
    title: str = Field(default="", description="Short story title")
    role: str = Field(default="", description="As a ...")
    action: str = Field(default="", description="I want to ...")
    value: str = Field(default="", description="so that ...")


class AcceptanceCriterion(BaseModel):
    """Single acceptance criterion in Given/When/Then format."""

    id: str = Field(default="", description="Unique AC ID, e.g., AC-001")
    given: str = Field(default="", description="Given context")
    when: str = Field(default="", description="When action")
    then: str = Field(default="", description="Then expected result")
    and_conditions: list[str] = Field(default_factory=list, description="Additional And conditions")


class AcceptanceCriteriaGroup(BaseModel):
    """Group of acceptance criteria for a user story."""

    story_id: str = Field(default="", description="Linked user story ID")
    story_title: str = Field(default="", description="Linked user story title")
    criteria: list[AcceptanceCriterion] = Field(
        default_factory=list, description="List of criteria"
    )


class ApiSpec(BaseModel):
    """API specification for an endpoint."""

    name: str = Field(default="", description="API operation name")
    method: str = Field(default="", description="HTTP method")
    path: str = Field(default="", description="URL path")
    permission_required: str | None = Field(default=None, description="Required permission")
    request_schema: dict[str, Any] = Field(
        default_factory=dict, description="Request fields and types"
    )
    response_schema: dict[str, Any] = Field(
        default_factory=dict, description="Response fields and types"
    )
    error_codes: list[str | int] = Field(default_factory=list, description="Possible error codes")


class TestCase(BaseModel):
    """Test case derived from acceptance criteria."""

    id: str = Field(default="", description="Unique test case ID, e.g., TC-001")
    title: str = Field(default="", description="Test case title")
    steps: list[str] = Field(default_factory=list, description="Test steps")
    expected_results: list[str] = Field(default_factory=list, description="Expected outcomes")
    related_ac: list[str] = Field(
        default_factory=list, description="Related acceptance criteria IDs"
    )


class Task(BaseModel):
    """Development task breakdown."""

    id: str = Field(default="", description="Unique task ID, e.g., TASK-001")
    title: str = Field(default="", description="Task title")
    type: str = Field(default="", description="Task type: backend, frontend, test, devops, docs")
    related_user_story: str = Field(default="", description="Linked user story ID")
    acceptance_criteria: list[str] = Field(default_factory=list, description="Linked AC IDs")
    estimated_effort: str = Field(
        default="medium", description="Effort estimate: small, medium, large"
    )
    files_to_modify: list[str] = Field(default_factory=list, description="Files to modify")
    out_of_scope: list[str] = Field(default_factory=list, description="Explicitly out of scope")


class AiCodingTask(BaseModel):
    """AI coding task package for an agent."""

    id: str = Field(default="", description="Task ID, matches Task.id")
    title: str = Field(default="", description="Task title")
    context: str = Field(default="", description="Business/technical context")
    goal: str = Field(default="", description="What the AI should achieve")
    requirements: list[str] = Field(default_factory=list, description="Specific requirements")
    acceptance_criteria: list[str] = Field(default_factory=list, description="Acceptance criteria")
    testing_requirements: list[str] = Field(
        default_factory=list, description="Testing expectations"
    )
    agent_instructions: list[str] = Field(
        default_factory=list, description="Instructions for the AI coding agent"
    )
    files_to_modify: list[str] = Field(default_factory=list, description="Files to modify")
    out_of_scope: list[str] = Field(default_factory=list, description="Out of scope items")


class ValidationReport(BaseModel):
    """Quality gate validation report."""

    passed: bool = Field(default=False, description="Overall pass status")
    traceability_issues: list[str] = Field(default_factory=list, description="Traceability gaps")
    completeness_issues: list[str] = Field(default_factory=list, description="Missing elements")
    safety_issues: list[str] = Field(default_factory=list, description="AI coding safety concerns")
    summary: str = Field(default="", description="Human-readable summary")
