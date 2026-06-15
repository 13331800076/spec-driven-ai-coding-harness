"""Tests for user story generator."""

import pytest

from spec_harness.generators.user_story_generator import UserStoryGenerator
from spec_harness.models import RequirementSpec, DomainAnalysis


@pytest.fixture
def generator():
    return UserStoryGenerator()


@pytest.fixture
def sample_spec():
    return RequirementSpec(
        requirement_id="REQ-TEST",
        title="Test Requirement",
        features=["upload attachments", "delete attachments", "preview attachments"],
        raw_text="Users should be able to upload, delete, and preview attachments.",
    )


@pytest.fixture
def sample_domain():
    return DomainAnalysis(
        operations=["upload", "delete", "preview"],
        business_objects=["attachment"],
        roles=["business_user"],
    )


def test_generate_stories(generator, sample_spec, sample_domain):
    stories = generator.generate(sample_spec, sample_domain)
    assert len(stories) == 3
    assert stories[0].id == "US-001"
    assert "upload" in stories[0].action.lower()
    assert stories[0].role == "business user"


def test_story_format(generator, sample_spec, sample_domain):
    stories = generator.generate(sample_spec, sample_domain)
    for story in stories:
        assert story.role
        assert story.action
        assert story.value
        assert story.id.startswith("US-")


def test_infer_features_when_empty(generator, sample_domain):
    spec = RequirementSpec(requirement_id="REQ-EMPTY", title="Empty", features=[], raw_text="")
    stories = generator.generate(spec, sample_domain)
    assert len(stories) > 0


def test_infer_value(generator, sample_spec, sample_domain):
    stories = generator.generate(sample_spec, sample_domain)
    upload_story = [s for s in stories if "upload" in s.action.lower()][0]
    assert "stored" in upload_story.value.lower() or "review" in upload_story.value.lower()
