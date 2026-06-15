"""Tests for requirement parser."""

import pytest
from pathlib import Path

from spec_harness.parser.requirement_parser import RequirementParser


@pytest.fixture
def parser():
    return RequirementParser()


@pytest.fixture
def sample_requirement(tmp_path: Path) -> str:
    content = """# Requirement: Unified Attachment Management

The system should provide a unified attachment management feature across procurement, sales, and inventory modules.

Users should be able to upload, preview, download, print, and delete attachments.

The system should support permission control. Only users with proper permissions can delete or print attachments.

The system should record audit logs for each attachment operation.
"""
    file_path = tmp_path / "attachment_management.md"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


def test_parse_normal_file(parser, sample_requirement):
    spec = parser.parse(sample_requirement)
    assert spec.title == "Requirement: Unified Attachment Management"
    assert "attachment" in spec.raw_text.lower()
    assert len(spec.features) > 0
    assert any("upload" in f.lower() for f in spec.features)


def test_parse_missing_file(parser):
    with pytest.raises(FileNotFoundError):
        parser.parse("/nonexistent/path.md")


def test_parse_empty_file(parser, tmp_path: Path):
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        parser.parse(str(empty_file))


def test_extract_actors(parser):
    text = "Users should be able to upload attachments. Sales users should approve orders."
    spec = parser._extract(text, "test")
    assert any("user" in a.lower() for a in spec.actors)
    assert any("sales" in a.lower() for a in spec.actors)


def test_extract_features(parser):
    text = """Users should be able to upload files.
    Users should be able to delete records.
    The system should support audit logging."""
    spec = parser._extract(text, "test")
    features_lower = [f.lower() for f in spec.features]
    assert any("upload" in f for f in features_lower)
    assert any("delete" in f for f in features_lower)


def test_extract_constraints(parser):
    text = "Only users with proper permissions can delete attachments. The system should record audit logs."
    spec = parser._extract(text, "test")
    constraints_lower = [c.lower() for c in spec.constraints]
    assert any("permission" in c for c in constraints_lower)
