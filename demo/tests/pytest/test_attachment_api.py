"""Tests for attachment APIs."""

import pytest
from fastapi.testclient import TestClient
from demo.implementation.main import app, attachments_db, audit_logs_db, USER_PERMISSIONS


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    attachments_db.clear()
    audit_logs_db.clear()
    yield


def test_upload_attachment_success():
    """Test successful upload with permission."""
    response = client.post(
        "/api/attachments",
        data={
            "business_object_type": "purchase_order",
            "business_object_id": "PO-1001",
        },
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "attachment_id" in data
    assert data["file_name"] == "test.pdf"


def test_upload_attachment_without_permission():
    """Test upload without permission."""
    # Temporarily modify user permissions
    original = USER_PERMISSIONS.get("user_1", []).copy()
    USER_PERMISSIONS["user_1"] = ["ATTACHMENT_PREVIEW"]  # No upload permission

    response = client.post(
        "/api/attachments",
        data={
            "business_object_type": "purchase_order",
            "business_object_id": "PO-1001",
        },
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 403

    USER_PERMISSIONS["user_1"] = original


def test_delete_attachment_success():
    """Test successful deletion with permission."""
    # First upload
    upload_resp = client.post(
        "/api/attachments",
        data={
            "business_object_type": "purchase_order",
            "business_object_id": "PO-1001",
        },
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_resp.json()["attachment_id"]

    # Then delete
    response = client.delete(f"/api/attachments/{attachment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_delete_attachment_without_permission():
    """Test deletion without permission."""
    original = USER_PERMISSIONS.get("user_1", []).copy()
    USER_PERMISSIONS["user_1"] = ["ATTACHMENT_PREVIEW"]  # No delete permission

    response = client.delete("/api/attachments/nonexistent")
    assert response.status_code == 403

    USER_PERMISSIONS["user_1"] = original


def test_delete_nonexistent_attachment():
    """Test deletion of non-existent attachment."""
    response = client.delete("/api/attachments/nonexistent-id")
    assert response.status_code == 404


def test_list_attachments():
    """Test listing attachments."""
    # Upload a file first
    client.post(
        "/api/attachments",
        data={
            "business_object_type": "purchase_order",
            "business_object_id": "PO-1001",
        },
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )

    response = client.get("/api/attachments")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["items"]) >= 1


def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
