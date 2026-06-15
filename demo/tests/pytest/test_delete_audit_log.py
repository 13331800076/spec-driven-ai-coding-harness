"""Tests for delete_audit_log API."""


def test_delete_audit_log_success(client, auth_headers):
    """Test successful delete_audit_log operation."""
    response = client.delete(
        "/api/audit_logs/{audit_log_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_delete_audit_log_unauthorized(client):
    """Test delete_audit_log without authentication."""
    response = client.delete(
        "/api/audit_logs/{audit_log_id}",
    )
    assert response.status_code == 401


def test_delete_audit_log_forbidden(client, auth_headers):
    """Test delete_audit_log with insufficient permissions."""
    # TODO: Mock user without AUDIT_LOG_DELETE permission
    response = client.delete(
        "/api/audit_logs/{audit_log_id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
