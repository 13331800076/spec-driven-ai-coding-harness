"""Tests for acceptance criteria generator."""

import pytest

from spec_harness.generators.acceptance_generator import AcceptanceCriteriaGenerator
from spec_harness.models import UserStory


@pytest.fixture
def generator():
    return AcceptanceCriteriaGenerator()


@pytest.fixture
def sample_stories():
    return [
        UserStory(
            id="US-001",
            title="Upload",
            role="user",
            action="upload attachments",
            value="store files",
        ),
        UserStory(
            id="US-002",
            title="Delete",
            role="admin",
            action="delete attachments",
            value="remove files",
        ),
    ]


def test_generate_acceptance_criteria(generator, sample_stories):
    groups = generator.generate(sample_stories)
    assert len(groups) == 2
    assert groups[0].story_id == "US-001"
    assert len(groups[0].criteria) >= 3


def test_criteria_format(generator, sample_stories):
    groups = generator.generate(sample_stories)
    for group in groups:
        for ac in group.criteria:
            assert ac.given.startswith("Given")
            assert ac.when.startswith("When")
            assert ac.then.startswith("Then")
            assert ac.id.startswith("AC-")


def test_audit_criteria_for_mutations(generator, sample_stories):
    groups = generator.generate(sample_stories)
    upload_group = [g for g in groups if g.story_id == "US-001"][0]
    audit_criteria = [
        ac for ac in upload_group.criteria if "audit" in ac.then.lower() or "log" in ac.then.lower()
    ]
    assert len(audit_criteria) > 0


def test_permission_failure_criteria(generator, sample_stories):
    groups = generator.generate(sample_stories)
    for group in groups:
        permission_criteria = [
            ac
            for ac in group.criteria
            if "permission" in ac.given.lower() or "not have" in ac.given.lower()
        ]
        assert len(permission_criteria) > 0
