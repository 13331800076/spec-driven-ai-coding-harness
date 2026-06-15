"""Validation and quality gate modules."""

from pathlib import Path
from typing import Any

from spec_harness.models import (
    RequirementSpec,
    UserStory,
    AcceptanceCriteriaGroup,
    TestCase,
    Task,
    AiCodingTask,
    ValidationReport,
)


class TraceabilityValidator:
    """Validate traceability from requirement to task."""

    def validate(
        self,
        spec: RequirementSpec,
        stories: list[UserStory],
        ac_groups: list[AcceptanceCriteriaGroup],
        test_cases: list[TestCase],
        tasks: list[Task],
    ) -> ValidationReport:
        issues: list[str] = []

        # Requirement -> Story traceability
        if not stories:
            issues.append("No user stories generated from requirement.")
        else:
            issues.extend(self._check_story_quality(stories))

        # Story -> AC traceability
        if not ac_groups:
            issues.append("No acceptance criteria generated.")
        else:
            issues.extend(self._check_ac_coverage(stories, ac_groups))

        # AC -> Test case traceability
        if not test_cases:
            issues.append("No test cases generated.")
        else:
            issues.extend(self._check_test_coverage(ac_groups, test_cases))

        # Task traceability
        if not tasks:
            issues.append("No tasks generated.")
        else:
            issues.extend(self._check_task_traceability(stories, tasks))

        passed = len(issues) == 0
        summary = "Validation passed." if passed else f"Found {len(issues)} issue(s)."

        return ValidationReport(
            passed=passed,
            traceability_issues=issues,
            completeness_issues=[],
            safety_issues=[],
            summary=summary,
        )

    def _check_story_quality(self, stories: list[UserStory]) -> list[str]:
        issues = []
        for story in stories:
            if not story.role:
                issues.append(f"{story.id} is missing a role.")
            if not story.action:
                issues.append(f"{story.id} is missing an action.")
            if not story.value:
                issues.append(f"{story.id} is missing a business value.")
        return issues

    def _check_ac_coverage(self, stories: list[UserStory], ac_groups: list[AcceptanceCriteriaGroup]) -> list[str]:
        issues = []
        story_ids = {s.id for s in stories}
        ac_story_ids = {g.story_id for g in ac_groups}
        missing = story_ids - ac_story_ids
        for sid in missing:
            issues.append(f"No acceptance criteria found for {sid}.")
        for group in ac_groups:
            if len(group.criteria) < 3:
                issues.append(f"{group.story_id} has only {len(group.criteria)} acceptance criteria (minimum 3 recommended).")
        return issues

    def _check_test_coverage(self, ac_groups: list[AcceptanceCriteriaGroup], test_cases: list[TestCase]) -> list[str]:
        issues = []
        ac_ids = {ac.id for group in ac_groups for ac in group.criteria}
        tc_ac_ids = set()
        for tc in test_cases:
            tc_ac_ids.update(tc.related_ac)
        missing = ac_ids - tc_ac_ids
        for ac_id in missing:
            issues.append(f"No test case covers acceptance criterion {ac_id}.")
        return issues

    def _check_task_traceability(self, stories: list[UserStory], tasks: list[Task]) -> list[str]:
        issues = []
        story_ids = {s.id for s in stories}
        for task in tasks:
            if task.related_user_story not in story_ids:
                issues.append(f"{task.id} is not linked to a valid user story.")
            if not task.acceptance_criteria:
                issues.append(f"{task.id} has no linked acceptance criteria.")
        return issues


class QualityGate:
    """Quality gate checks for AI coding safety."""

    def check(self, tasks: list[Task], ai_tasks: list[AiCodingTask]) -> ValidationReport:
        issues: list[str] = []

        for task in tasks:
            if not task.files_to_modify:
                issues.append(f"{task.id} does not specify files to modify.")
            if len(task.files_to_modify) > 5:
                issues.append(f"{task.id} modifies too many files ({len(task.files_to_modify)}), consider splitting.")
            if not task.out_of_scope:
                issues.append(f"{task.id} lacks explicit out-of-scope definition.")

        for ai_task in ai_tasks:
            if not ai_task.acceptance_criteria:
                issues.append(f"{ai_task.id} AI coding task lacks acceptance criteria.")
            if not ai_task.testing_requirements:
                issues.append(f"{ai_task.id} AI coding task lacks testing requirements.")
            vague_keywords = ["optimize", "improve", "refactor", "clean up", "enhance"]
            for keyword in vague_keywords:
                if keyword in ai_task.title.lower() or keyword in ai_task.goal.lower():
                    issues.append(f"{ai_task.id} contains vague keyword '{keyword}'. Use specific, measurable goals.")

        passed = len(issues) == 0
        summary = "Quality gate passed." if passed else f"Quality gate found {len(issues)} issue(s)."

        return ValidationReport(
            passed=passed,
            traceability_issues=[],
            completeness_issues=[],
            safety_issues=issues,
            summary=summary,
        )
