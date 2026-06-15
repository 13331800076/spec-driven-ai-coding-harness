"""Tests for list_attachment_operation API."""


def test_list_attachment_operation_success(client, auth_headers):
    """Test successful list_attachment_operation operation."""
    response = client.get(
        "/api/attachment_operations",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_list_attachment_operation_unauthorized(client):
    """Test list_attachment_operation without authentication."""
    response = client.get(
        "/api/attachment_operations",
    )
    assert response.status_code == 401


def test_list_attachment_operation_forbidden(client, auth_headers):
    """Test list_attachment_operation with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_OPERATION_LIST permission
    response = client.get(
        "/api/attachment_operations",
        headers=auth_headers,
    )
    assert response.status_code == 403
