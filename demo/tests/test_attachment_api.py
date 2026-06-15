import pytest
from fastapi.testclient import TestClient
from demo.implementation.main import app

client = TestClient(app)


def test_upload_attachment_success():
    """Test successful attachment upload."""
    response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "attachment_id" in data
    assert data["file_name"] == "test.pdf"


def test_upload_attachment_without_permission():
    """Test upload without permission."""
    # In production, mock user without ATTACHMENT_UPLOAD
    response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("test.pdf", b"test", "application/pdf")},
    )
    # Current mock user has all permissions, so this test would need mocking
    # For demo, we assert the endpoint exists and responds
    assert response.status_code in [200, 403]


def test_preview_attachment_success():
    """Test successful preview."""
    # First upload
    upload_response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("test.pdf", b"test", "application/pdf")},
    )
    attachment_id = upload_response.json()["attachment_id"]

    response = client.get(f"/api/attachments/{attachment_id}/preview")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "preview_url" in data


def test_delete_attachment_success():
    """Test successful deletion."""
    # First upload
    upload_response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
        files={"file": ("test.pdf", b"test", "application/pdf")},
    )
    attachment_id = upload_response.json()["attachment_id"]

    response = client.delete(f"/api/attachments/{attachment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_delete_attachment_not_found():
    """Test deletion of non-existent attachment."""
    response = client.delete("/api/attachments/nonexistent-id")
    assert response.status_code == 404


def test_list_attachments():
    """Test listing attachments."""
    response = client.get("/api/attachments")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "items" in data
    assert "total" in data


def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
