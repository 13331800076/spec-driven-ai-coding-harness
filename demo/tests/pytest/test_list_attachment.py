"""Tests for list_attachment API."""


def test_list_attachment_success(client, auth_headers):
    """Test successful list_attachment operation."""
    response = client.get(
        "/api/attachments",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_list_attachment_unauthorized(client):
    """Test list_attachment without authentication."""
    response = client.get(
        "/api/attachments",
    )
    assert response.status_code == 401


def test_list_attachment_forbidden(client, auth_headers):
    """Test list_attachment with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_LIST permission
    response = client.get(
        "/api/attachments",
        headers=auth_headers,
    )
    assert response.status_code == 403
