"""Tests for API spec generator."""

import pytest

from spec_harness.generators.api_spec_generator import ApiSpecGenerator
from spec_harness.models import DomainAnalysis, RequirementSpec, UserStory


@pytest.fixture
def generator():
    return ApiSpecGenerator()


@pytest.fixture
def sample_spec():
    return RequirementSpec(
        requirement_id="REQ-TEST",
        title="Test Requirement",
        raw_text="Users should be able to upload and delete attachments.",
    )


@pytest.fixture
def sample_domain():
    return DomainAnalysis(
        operations=["upload", "delete", "list"],
        business_objects=["attachment"],
        roles=["user"],
    )


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
    ]


def test_generate_api_specs(generator, sample_spec, sample_domain, sample_stories):
    apis = generator.generate(sample_spec, sample_domain, sample_stories)
    assert len(apis) > 0
    names = [a.name for a in apis]
    assert any("upload" in n for n in names)
    assert any("delete" in n for n in names)


def test_api_spec_structure(generator, sample_spec, sample_domain, sample_stories):
    apis = generator.generate(sample_spec, sample_domain, sample_stories)
    for api in apis:
        assert api.method in ("GET", "POST", "PUT", "DELETE")
        assert api.path.startswith("/api/")
        assert api.permission_required
        assert api.response_schema


def test_error_codes(generator, sample_spec, sample_domain, sample_stories):
    apis = generator.generate(sample_spec, sample_domain, sample_stories)
    for api in apis:
        assert "400" in api.error_codes
        assert "401" in api.error_codes
        assert "500" in api.error_codes
