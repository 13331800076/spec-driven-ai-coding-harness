"""Tests for upload_audit_log API."""


def test_upload_audit_log_success(client, auth_headers):
    """Test successful upload_audit_log operation."""
    response = client.post(
        "/api/audit_logs/upload",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_upload_audit_log_unauthorized(client):
    """Test upload_audit_log without authentication."""
    response = client.post(
        "/api/audit_logs/upload",
    )
    assert response.status_code == 401


def test_upload_audit_log_forbidden(client, auth_headers):
    """Test upload_audit_log with insufficient permissions."""
    # TODO: Mock user without AUDIT_LOG_UPLOAD permission
    response = client.post(
        "/api/audit_logs/upload",
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_upload_audit_log_validation_error(client, auth_headers):
    """Test upload_audit_log with invalid request payload."""
    response = client.post(
        "/api/audit_logs/upload",
        headers=auth_headers,
        json={"invalid": "data"},
    )
    assert response.status_code == 400
