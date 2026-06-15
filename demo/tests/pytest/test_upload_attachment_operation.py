"""Tests for upload_attachment_operation API."""


def test_upload_attachment_operation_success(client, auth_headers):
    """Test successful upload_attachment_operation operation."""
    response = client.post(
        "/api/attachment_operations/upload",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_upload_attachment_operation_unauthorized(client):
    """Test upload_attachment_operation without authentication."""
    response = client.post(
        "/api/attachment_operations/upload",
    )
    assert response.status_code == 401


def test_upload_attachment_operation_forbidden(client, auth_headers):
    """Test upload_attachment_operation with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_OPERATION_UPLOAD permission
    response = client.post(
        "/api/attachment_operations/upload",
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_upload_attachment_operation_validation_error(client, auth_headers):
    """Test upload_attachment_operation with invalid request payload."""
    response = client.post(
        "/api/attachment_operations/upload",
        headers=auth_headers,
        json={"invalid": "data"},
    )
    assert response.status_code == 400
