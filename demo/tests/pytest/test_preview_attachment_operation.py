"""Tests for preview_attachment_operation API."""


def test_preview_attachment_operation_success(client, auth_headers):
    """Test successful preview_attachment_operation operation."""
    response = client.get(
        "/api/attachment_operations/{attachment_operation_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_preview_attachment_operation_unauthorized(client):
    """Test preview_attachment_operation without authentication."""
    response = client.get(
        "/api/attachment_operations/{attachment_operation_id}",
    )
    assert response.status_code == 401


def test_preview_attachment_operation_forbidden(client, auth_headers):
    """Test preview_attachment_operation with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_OPERATION_PREVIEW permission
    response = client.get(
        "/api/attachment_operations/{attachment_operation_id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
