"""AI coding task generator module."""

from spec_harness.models import Task, AiCodingTask


class AgentTaskGenerator:
    """Generate AI coding task packages from development tasks."""

    def generate(self, tasks: list[Task]) -> list[AiCodingTask]:
        return [self._convert_task(task) for task in tasks]

    def _convert_task(self, task: Task) -> AiCodingTask:
        context = self._build_context(task)
        goal = f"Complete {task.title.lower()} with proper tests and validation."
        requirements = self._build_requirements(task)
        testing_requirements = self._build_testing_requirements(task)
        agent_instructions = [
            "Do not modify unrelated modules.",
            "Add tests before implementation where possible.",
            "Follow existing code style and conventions.",
            "Keep changes focused and minimal.",
            "Ensure all acceptance criteria are met.",
        ]

        return AiCodingTask(
            id=task.id,
            title=task.title,
            context=context,
            goal=goal,
            requirements=requirements,
            acceptance_criteria=task.acceptance_criteria,
            testing_requirements=testing_requirements,
            agent_instructions=agent_instructions,
            files_to_modify=task.files_to_modify,
            out_of_scope=task.out_of_scope,
        )

    def _build_context(self, task: Task) -> str:
        return (
            f"This task is part of a feature implementation. "
            f"Task type: {task.type}. "
            f"Related story: {task.related_user_story}. "
            f"Focus on completing the specified scope with high quality."
        )

    def _build_requirements(self, task: Task) -> list[str]:
        reqs = [f"Implement {task.title}."]
        if task.acceptance_criteria:
            reqs.append("Meet all linked acceptance criteria.")
        reqs.append("Ensure code is testable and follows project conventions.")
        return reqs

    def _build_testing_requirements(self, task: Task) -> list[str]:
        reqs = ["Add unit tests for new logic."]
        if task.type == "backend":
            reqs.append("Add API integration tests if applicable.")
        if task.type == "frontend":
            reqs.append("Add component tests or E2E tests if applicable.")
        reqs.append("Ensure tests cover success and failure paths.")
        return reqs
