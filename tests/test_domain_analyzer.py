"""Tests for domain analyzer."""

import pytest

from spec_harness.analyzer.domain_analyzer import DomainAnalyzer
from spec_harness.models import RequirementSpec


@pytest.fixture
def analyzer():
    return DomainAnalyzer()


@pytest.fixture
def attachment_spec():
    return RequirementSpec(
        requirement_id="REQ-ATTACHMENT",
        title="Unified Attachment Management",
        raw_text=(  # noqa: E501
            """Users should be able to upload, preview, download, print, and delete attachments.
        Only users with proper permissions can delete or print attachments.
        The system should record audit logs for each attachment operation."""
        ),
        actors=["user"],
        business_objects=["attachment", "audit_log"],
        features=[
            "upload attachments",
            "preview attachments",
            "download attachments",
            "print attachments",
            "delete attachments",
        ],
        constraints=["Only users with proper permissions can delete or print attachments"],
    )


@pytest.fixture
def customer_spec():
    return RequirementSpec(
        requirement_id="REQ-CUSTOMER",
        title="Customer Management",
        raw_text=(
            """Users should be able to create, update, view, and delete customer records.
        The system should support customer classification and tagging.
        The system should enforce data validation: phone numbers must be valid, email must be unique."""  # noqa: E501
        ),
        actors=["user"],
        business_objects=["customer"],
        features=["create customer", "update customer", "view customer", "delete customer"],
        constraints=["phone numbers must be valid", "email must be unique"],
    )


def test_analyze_attachment_domain(analyzer, attachment_spec):
    domain = analyzer.analyze(attachment_spec)
    assert "upload" in domain.operations
    assert "delete" in domain.operations
    assert "preview" in domain.operations
    assert "attachment" in domain.business_objects
    assert any("ATTACHMENT" in p for p in domain.permissions)


def test_analyze_customer_domain(analyzer, customer_spec):
    domain = analyzer.analyze(customer_spec)
    assert "create" in domain.operations
    assert "update" in domain.operations
    assert "customer" in domain.business_objects
    assert any("CUSTOMER" in p for p in domain.permissions)


def test_extract_modules(analyzer, attachment_spec):
    # Add explicit module mentions to the raw text for this test
    attachment_spec.raw_text += " This feature spans procurement, sales, and inventory modules."
    domain = analyzer.analyze(attachment_spec)
    assert any(m in domain.modules for m in ["sales", "inventory", "procurement"])


def test_extract_roles(analyzer, attachment_spec):
    domain = analyzer.analyze(attachment_spec)
    assert len(domain.roles) > 0


def test_extract_constraints(analyzer, attachment_spec):
    domain = analyzer.analyze(attachment_spec)
    assert len(domain.constraints) > 0
    assert any("permission" in c.lower() for c in domain.constraints)
