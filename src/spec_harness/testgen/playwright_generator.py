"""Playwright skeleton generator module."""

from pathlib import Path

from spec_harness.models import UserStory


class PlaywrightGenerator:
    """Generate Playwright test skeleton files from user stories."""

    def generate(self, stories: list[UserStory], output_dir: Path) -> None:
        test_dir = output_dir / "playwright"
        test_dir.mkdir(parents=True, exist_ok=True)

        for story in stories:
            test_file = test_dir / f"test_{story.id.lower().replace('-', '_')}.py"
            test_file.write_text(self._test_file_content(story), encoding="utf-8")

    def _test_file_content(self, story: UserStory) -> str:
        action_slug = story.action.replace(" ", "_").lower()[:30]
        return f'''"""E2E test for {story.id}: {story.title}."""

from playwright.sync_api import Page, expect


def test_{action_slug}(page: Page):
    """{story.id}: {story.title}"""
    # TODO: Navigate to the relevant page
    page.goto("/")

    # TODO: Perform the action as a {story.role}
    # page.get_by_test_id("some-element").click()

    # TODO: Assert expected outcome
    # expect(page.get_by_test_id("success-indicator")).to_be_visible()

    raise NotImplementedError("Implement E2E test for {story.action}")
'''
