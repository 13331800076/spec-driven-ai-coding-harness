"""Tests for preview_audit_log API."""


def test_preview_audit_log_success(client, auth_headers):
    """Test successful preview_audit_log operation."""
    response = client.get(
        "/api/audit_logs/{audit_log_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_preview_audit_log_unauthorized(client):
    """Test preview_audit_log without authentication."""
    response = client.get(
        "/api/audit_logs/{audit_log_id}",
    )
    assert response.status_code == 401


def test_preview_audit_log_forbidden(client, auth_headers):
    """Test preview_audit_log with insufficient permissions."""
    # TODO: Mock user without AUDIT_LOG_PREVIEW permission
    response = client.get(
        "/api/audit_logs/{audit_log_id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
