"""Shared pytest fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add demo implementation to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "implementation"))

from main import app, attachments_db, audit_logs_db


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Authenticated request headers."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test."""
    attachments_db.clear()
    audit_logs_db.clear()
    yield
    attachments_db.clear()
    audit_logs_db.clear()
