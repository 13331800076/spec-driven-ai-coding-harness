"""Tests for delete_attachment API."""


def test_delete_attachment_success(client, auth_headers):
    """Test successful delete_attachment operation."""
    response = client.delete(
        "/api/attachments/{attachment_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_delete_attachment_unauthorized(client):
    """Test delete_attachment without authentication."""
    response = client.delete(
        "/api/attachments/{attachment_id}",
    )
    assert response.status_code == 401


def test_delete_attachment_forbidden(client, auth_headers):
    """Test delete_attachment with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_DELETE permission
    response = client.delete(
        "/api/attachments/{attachment_id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
