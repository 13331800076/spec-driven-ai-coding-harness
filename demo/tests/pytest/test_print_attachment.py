"""Tests for print_attachment API."""


def test_print_attachment_success(client, auth_headers):
    """Test successful print_attachment operation."""
    response = client.post(
        "/api/attachments/print",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_print_attachment_unauthorized(client):
    """Test print_attachment without authentication."""
    response = client.post(
        "/api/attachments/print",
    )
    assert response.status_code == 401


def test_print_attachment_forbidden(client, auth_headers):
    """Test print_attachment with insufficient permissions."""
    # TODO: Mock user without ATTACHMENT_PRINT permission
    response = client.post(
        "/api/attachments/print",
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_print_attachment_validation_error(client, auth_headers):
    """Test print_attachment with invalid request payload."""
    response = client.post(
        "/api/attachments/print",
        headers=auth_headers,
        json={"invalid": "data"},
    )
    assert response.status_code == 400
