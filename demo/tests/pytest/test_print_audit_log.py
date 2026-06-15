"""Tests for print_audit_log API."""


def test_print_audit_log_success(client, auth_headers):
    """Test successful print_audit_log operation."""
    response = client.post(
        "/api/audit_logs/print",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_print_audit_log_unauthorized(client):
    """Test print_audit_log without authentication."""
    response = client.post(
        "/api/audit_logs/print",
    )
    assert response.status_code == 401


def test_print_audit_log_forbidden(client, auth_headers):
    """Test print_audit_log with insufficient permissions."""
    # TODO: Mock user without AUDIT_LOG_PRINT permission
    response = client.post(
        "/api/audit_logs/print",
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_print_audit_log_validation_error(client, auth_headers):
    """Test print_audit_log with invalid request payload."""
    response = client.post(
        "/api/audit_logs/print",
        headers=auth_headers,
        json={"invalid": "data"},
    )
    assert response.status_code == 400
