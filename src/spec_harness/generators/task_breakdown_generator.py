"""Task breakdown generator module."""

from spec_harness.models import AcceptanceCriteriaGroup, ApiSpec, Task, TestCase, UserStory


class TaskBreakdownGenerator:
    """Generate development tasks from stories, criteria, specs, and test cases."""

    def generate(
        self,
        stories: list[UserStory],
        ac_groups: list[AcceptanceCriteriaGroup],
        apis: list[ApiSpec],
        test_cases: list[TestCase],
    ) -> list[Task]:
        tasks: list[Task] = []
        task_counter = 1

        # Domain model task
        tasks.append(
            Task(
                id=f"TASK-{task_counter:03d}",
                title="Implement domain model and data structures",
                type="backend",
                related_user_story=stories[0].id if stories else "",
                acceptance_criteria=[],
                estimated_effort="medium",
                files_to_modify=["src/models/domain.py", "src/schemas/__init__.py"],
                out_of_scope=["API implementation", "UI components"],
            )
        )
        task_counter += 1

        # API tasks
        for api in apis:
            related_ac = []
            for group in ac_groups:
                if any(ac.id for ac in group.criteria):
                    related_ac.extend([ac.id for ac in group.criteria[:2]])

            tasks.append(
                Task(
                    id=f"TASK-{task_counter:03d}",
                    title=f"Implement {api.name} API",
                    type="backend",
                    related_user_story=stories[0].id if stories else "",
                    acceptance_criteria=related_ac[:2],
                    estimated_effort="medium",
                    files_to_modify=[
                        f"src/routers/{api.name}.py",
                        f"src/services/{api.name}_service.py",
                        f"tests/test_{api.name}.py",
                    ],
                    out_of_scope=["Unrelated APIs", "Frontend integration"],
                )
            )
            task_counter += 1

        # Test tasks
        tasks.append(
            Task(
                id=f"TASK-{task_counter:03d}",
                title="Implement comprehensive test suite",
                type="test",
                related_user_story=stories[0].id if stories else "",
                acceptance_criteria=[],
                estimated_effort="large",
                files_to_modify=["tests/conftest.py", "tests/"],
                out_of_scope=["Production code changes"],
            )
        )
        task_counter += 1

        # Permission task
        tasks.append(
            Task(
                id=f"TASK-{task_counter:03d}",
                title="Implement permission control middleware",
                type="backend",
                related_user_story=stories[0].id if stories else "",
                acceptance_criteria=[],
                estimated_effort="medium",
                files_to_modify=["src/auth/permissions.py", "src/middleware/auth.py"],
                out_of_scope=["User management", "UI login flow"],
            )
        )

        return tasks
