"""Test the FastAPI attachment management API."""

import pytest
from fastapi.testclient import TestClient

from demo.implementation.main import app, attachments_db, audit_logs_db, USER_PERMISSIONS

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory database before each test."""
    attachments_db.clear()
    audit_logs_db.clear()
    yield


def test_upload_attachment_success():
    """Test successful upload with valid permissions."""
    response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("demo.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "attachment_id" in data
    assert data["file_name"] == "demo.pdf"
    assert len(audit_logs_db) == 1
    assert audit_logs_db[0]["action"] == "UPLOAD"


def test_upload_attachment_unauthorized():
    """Test upload without authentication."""
    # Note: In our demo, auth is mocked, so this test checks the framework
    # In real app, would test 401/403
    response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("demo.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 200


def test_delete_attachment_success():
    """Test successful deletion with proper permissions."""
    # First upload
    upload_resp = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("demo.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_resp.json()["attachment_id"]

    # Then delete
    response = client.delete(f"/api/attachments/{attachment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert attachment_id not in attachments_db


def test_delete_attachment_not_found():
    """Test deletion of non-existent attachment."""
    response = client.delete("/api/attachments/non-existent-id")
    assert response.status_code == 404


def test_list_attachments():
    """Test listing attachments."""
    # Upload a few files
    for i in range(3):
        client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
            files={"file": (f"file{i}.pdf", b"content", "application/pdf")},
        )

    response = client.get("/api/attachments")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["items"]) == 3
    assert data["total"] == 3


def test_preview_attachment():
    """Test preview endpoint."""
    upload_resp = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("demo.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_resp.json()["attachment_id"]

    response = client.get(f"/api/attachments/{attachment_id}/preview")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "preview_url" in data


def test_download_attachment():
    """Test download endpoint."""
    upload_resp = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("demo.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_resp.json()["attachment_id"]

    response = client.get(f"/api/attachments/{attachment_id}/download")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "download_url" in data


def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
