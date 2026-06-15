"""Tests for the attachment management API demo implementation."""

import pytest
from fastapi.testclient import TestClient
from demo.implementation.main import app, attachments_db, audit_logs_db, USER_PERMISSIONS

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    attachments_db.clear()
    audit_logs_db.clear()


class TestUploadAttachment:
    def test_upload_success(self):
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

    def test_upload_without_permission(self):
        # Mock user without upload permission
        original = USER_PERMISSIONS.copy()
        USER_PERMISSIONS["user_1"] = ["ATTACHMENT_PREVIEW"]  # Remove upload permission

        response = client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
            files={"file": ("test.pdf", b"test content", "application/pdf")},
        )
        assert response.status_code == 403

        USER_PERMISSIONS.update(original)


class TestDeleteAttachment:
    def test_delete_success(self):
        # First upload
        upload_response = client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
            files={"file": ("test.pdf", b"test content", "application/pdf")},
        )
        attachment_id = upload_response.json()["attachment_id"]

        # Then delete
        response = client.delete(f"/api/attachments/{attachment_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_delete_not_found(self):
        response = client.delete("/api/attachments/nonexistent-id")
        assert response.status_code == 404


class TestPreviewAttachment:
    def test_preview_success(self):
        upload_response = client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
            files={"file": ("test.pdf", b"test content", "application/pdf")},
        )
        attachment_id = upload_response.json()["attachment_id"]

        response = client.get(f"/api/attachments/{attachment_id}/preview")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "preview_url" in response.json()


class TestListAttachments:
    def test_list_empty(self):
        response = client.get("/api/attachments")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["total"] == 0
        assert data["items"] == []

    def test_list_with_items(self):
        client.post(
            "/api/attachments",
            data={"business_object_type": "purchase_order", "business_object_id": "PO-1001"},
            files={"file": ("test.pdf", b"test content", "application/pdf")},
        )

        response = client.get("/api/attachments")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
