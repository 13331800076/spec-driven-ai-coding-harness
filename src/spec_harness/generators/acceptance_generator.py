"""Acceptance criteria generator module."""

from spec_harness.models import AcceptanceCriteriaGroup, AcceptanceCriterion, UserStory


class AcceptanceCriteriaGenerator:
    """Generate Given/When/Then acceptance criteria for user stories."""

    def generate(self, stories: list[UserStory]) -> list[AcceptanceCriteriaGroup]:
        groups: list[AcceptanceCriteriaGroup] = []
        for story in stories:
            criteria = self._generate_for_story(story)
            groups.append(
                AcceptanceCriteriaGroup(
                    story_id=story.id,
                    story_title=story.title,
                    criteria=criteria,
                )
            )
        return groups

    def _generate_for_story(self, story: UserStory) -> list[AcceptanceCriterion]:
        criteria: list[AcceptanceCriterion] = []
        action = story.action.lower()
        role = story.role

        # 1. Success path
        criteria.append(
            AcceptanceCriterion(
                id=f"AC-{story.id.split('-')[1]}-001",
                given=f"Given a {role} has the necessary permissions",
                when=f"When the {role} attempts to {action}",
                then="Then the operation should complete successfully",
                and_conditions=[
                    "And the result should be consistent with the expected outcome",
                    "And the system state should be updated accordingly",
                ],
            )
        )

        # 2. Permission failure
        criteria.append(
            AcceptanceCriterion(
                id=f"AC-{story.id.split('-')[1]}-002",
                given=f"Given a {role} does not have the required permission",
                when=f"When the {role} attempts to {action}",
                then="Then the system should reject the operation",
                and_conditions=[
                    "And a permission denied message should be returned",
                    "And no unauthorized change should occur",
                ],
            )
        )

        # 3. Validation / error case
        criteria.append(
            AcceptanceCriterion(
                id=f"AC-{story.id.split('-')[1]}-003",
                given=f"Given a {role} provides invalid or incomplete data",
                when=f"When the {role} attempts to {action}",
                then="Then the system should validate the input",
                and_conditions=[
                    "And appropriate error messages should be returned",
                    "And the operation should not proceed with invalid data",
                ],
            )
        )

        # 4. Audit / logging when applicable
        if any(
            kw in action for kw in ("upload", "delete", "update", "create", "approve", "reject")
        ):
            criteria.append(
                AcceptanceCriterion(
                    id=f"AC-{story.id.split('-')[1]}-004",
                    given=f"Given a {role} successfully performs the operation",
                    when="When the operation completes",
                    then="Then the system should record an audit log",
                    and_conditions=[
                        "And the log should include the user identifier",
                        "And the log should include a timestamp of the operation",
                    ],
                )
            )

        return criteria
