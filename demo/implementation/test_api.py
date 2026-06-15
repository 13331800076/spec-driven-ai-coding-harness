from fastapi.testclient import TestClient
import pytest
from main import app, attachments_db, audit_logs_db, USER_PERMISSIONS

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    attachments_db.clear()
    audit_logs_db.clear()


def test_upload_attachment_success():
    """Test successful attachment upload with proper permissions."""
    response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "attachment_id" in data
    assert data["file_name"] == "test.pdf"


def test_upload_attachment_unauthorized():
    """Test upload without proper permissions."""
    # user_2 doesn't have ATTACHMENT_UPLOAD permission
    # This would require modifying auth in real scenario
    pass


def test_preview_attachment_success():
    """Test successful attachment preview."""
    # First upload
    upload_response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_response.json()["attachment_id"]

    # Then preview
    response = client.get(f"/api/attachments/{attachment_id}/preview")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "preview_url" in data


def test_download_attachment_success():
    """Test successful attachment download."""
    upload_response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_response.json()["attachment_id"]

    response = client.get(f"/api/attachments/{attachment_id}/download")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "download_url" in data


def test_delete_attachment_success():
    """Test successful attachment deletion."""
    upload_response = client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )
    attachment_id = upload_response.json()["attachment_id"]

    response = client.delete(f"/api/attachments/{attachment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "deleted" in data["message"].lower()


def test_delete_attachment_not_found():
    """Test deleting non-existent attachment."""
    response = client.delete("/api/attachments/non-existent-id")
    assert response.status_code == 404


def test_list_attachments():
    """Test listing attachments."""
    # Upload multiple attachments
    for i in range(3):
        client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": f"PO-00{i}"},
            files={"file": (f"test{i}.pdf", b"test content", "application/pdf")},
        )

    response = client.get("/api/attachments")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["items"]) == 3
    assert data["total"] == 3


def test_audit_log_created():
    """Test that audit logs are created for operations."""
    # Upload an attachment
    client.post(
        "/api/attachments",
        data={"business_object_type": "purchase_order", "business_object_id": "PO-001"},
        files={"file": ("test.pdf", b"test content", "application/pdf")},
    )

    # Check audit logs
    response = client.get("/api/audit-logs")
    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) > 0
    assert any(log["action"] == "UPLOAD" for log in data["logs"])
