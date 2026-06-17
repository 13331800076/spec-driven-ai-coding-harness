"""Test case generator module."""

from spec_harness.models import AcceptanceCriteriaGroup, ApiSpec, TestCase


class TestCaseGenerator:
    """Generate test cases from acceptance criteria and API specs."""

    def generate(
        self, ac_groups: list[AcceptanceCriteriaGroup], apis: list[ApiSpec]
    ) -> list[TestCase]:
        test_cases: list[TestCase] = []
        tc_counter = 1

        for group in ac_groups:
            for ac in group.criteria:
                tc = self._build_test_case(ac, group.story_id, tc_counter)
                test_cases.append(tc)
                tc_counter += 1

        # Add API-level test cases
        for api in apis:
            tc = self._build_api_test_case(api, tc_counter)
            test_cases.append(tc)
            tc_counter += 1

        return test_cases

    def _build_test_case(self, ac, story_id: str, counter: int) -> TestCase:
        permission = "relevant permission"
        if "does not have" in ac.given:
            permission = "without the required permission"
        elif "has" in ac.given:
            permission = "with the required permission"

        steps = [
            f"Login as a user {permission}.",
            "Navigate to the relevant feature area.",
            f"{ac.when}.",
            "Observe the system response.",
        ]

        expected_results = [
            f"{ac.then}.",
        ]
        for condition in ac.and_conditions:
            expected_results.append(f"{condition}.")

        return TestCase(
            id=f"TC-{counter:03d}",
            title=f"{story_id} - {ac.id} validation",
            steps=steps,
            expected_results=expected_results,
            related_ac=[ac.id],
        )

    def _build_api_test_case(self, api: ApiSpec, counter: int) -> TestCase:
        steps = [
            f"Prepare authentication with {api.permission_required or 'valid credentials'}.",
            f"Send {api.method} request to {api.path}.",
            "Include valid request payload.",
            "Verify response status and body.",
        ]

        expected_results = [
            "Response status is appropriate for the scenario.",
            f"Response body contains required fields: {', '.join(api.response_schema.keys())}.",
        ]

        return TestCase(
            id=f"TC-{counter:03d}",
            title=f"API {api.name} basic functionality",
            steps=steps,
            expected_results=expected_results,
            related_ac=[],
        )
