"""Tests for download_attachment API."""


def test_download_attachment_success(client, auth_headers):
    """Test successful download_attachment operation."""
    response = client.get(
        "/api/attachments/{attachment_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_download_attachment_unauthorized(client):
    """Test download_attachment without authentication."""
    response = client.get(
        "/api/attachments/{attachment_id}",
    )
    assert response.status_code == 401


def test_download_attachment_forbidden(client, auth_headers):
    """Test download_attachment with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_DOWNLOAD permission
    response = client.get(
        "/api/attachments/{attachment_id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
