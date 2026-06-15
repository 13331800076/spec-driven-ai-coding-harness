"""Tests for task breakdown generator."""

import pytest

from spec_harness.generators.task_breakdown_generator import TaskBreakdownGenerator
from spec_harness.models import UserStory, AcceptanceCriteriaGroup, AcceptanceCriterion, ApiSpec, TestCase


@pytest.fixture
def generator():
    return TaskBreakdownGenerator()


@pytest.fixture
def sample_stories():
    return [
        UserStory(id="US-001", title="Upload", role="user", action="upload attachments", value="store files"),
    ]


@pytest.fixture
def sample_ac_groups():
    return [
        AcceptanceCriteriaGroup(
            story_id="US-001",
            story_title="Upload",
            criteria=[
                AcceptanceCriterion(id="AC-001", given="Given user", when="When upload", then="Then success"),
            ],
        ),
    ]


@pytest.fixture
def sample_apis():
    return [
        ApiSpec(name="upload_attachment", method="POST", path="/api/attachments/upload", permission_required="ATTACHMENT_UPLOAD"),
    ]


@pytest.fixture
def sample_test_cases():
    return [
        TestCase(id="TC-001", title="Upload success", steps=["1. Login", "2. Upload"], expected_results=["Success"]),
    ]


def test_generate_tasks(generator, sample_stories, sample_ac_groups, sample_apis, sample_test_cases):
    tasks = generator.generate(sample_stories, sample_ac_groups, sample_apis, sample_test_cases)
    assert len(tasks) > 0
    assert all(t.id.startswith("TASK-") for t in tasks)


def test_task_has_related_story(generator, sample_stories, sample_ac_groups, sample_apis, sample_test_cases):
    tasks = generator.generate(sample_stories, sample_ac_groups, sample_apis, sample_test_cases)
    for task in tasks:
        assert task.related_user_story == "US-001"


def test_task_has_files(generator, sample_stories, sample_ac_groups, sample_apis, sample_test_cases):
    tasks = generator.generate(sample_stories, sample_ac_groups, sample_apis, sample_test_cases)
    api_task = [t for t in tasks if "API" in t.title or "upload" in t.title.lower()]
    assert len(api_task) > 0
    assert len(api_task[0].files_to_modify) > 0
