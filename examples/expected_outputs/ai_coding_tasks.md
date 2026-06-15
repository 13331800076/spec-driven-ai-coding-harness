# AI Coding Tasks

## TASK-002: Implement upload attachment API

Context:
The system needs a unified attachment upload API for multiple ERP modules (procurement, sales, inventory). Users upload files that are linked to business documents via business_object_type and business_object_id.

Goal:
Implement a POST /api/attachments endpoint that accepts file uploads, validates permissions, stores files, and creates audit logs.

Requirements:
- Validate that the user has ATTACHMENT_UPLOAD permission before processing the upload.
- Accept business_object_type and business_object_id in the request form data.
- Validate file type (allow PDF, PNG, JPG, DOCX, XLSX only).
- Store file metadata in the database (file_name, file_size, mime_type, storage_path).
- Save the actual file to a configurable storage directory.
- Link the attachment record to the business object via business_object_type and business_object_id.
- Create an audit log entry after successful upload with user_id, timestamp, action='UPLOAD', and attachment_id.

Acceptance Criteria:
- Upload succeeds for users with ATTACHMENT_UPLOAD permission and returns attachment_id.
- Invalid file type is rejected with a 400 Bad Request error.
- Missing business_object_type or business_object_id is rejected with a 400 error.
- Users without ATTACHMENT_UPLOAD permission receive a 403 Forbidden error.
- Audit log is created with correct user_id, timestamp, and action='UPLOAD'.

Testing:
- Add pytest test for successful upload with valid PDF file.
- Add pytest test for invalid file type rejection.
- Add pytest test for missing permission (403).
- Add pytest test for missing business_object_id.
- Add pytest test for audit log creation after successful upload.

Instructions for AI Coding Agent:
- Do not modify unrelated modules (e.g., user management, inventory service).
- Add tests before or alongside implementation.
- Keep API response format consistent with api_spec.yaml.
- Use dependency injection for the storage service so it can be mocked in tests.
- Ensure file cleanup in test teardown to avoid disk pollution.

Files to modify:
- src/routers/attachments.py
- src/services/attachment_service.py
- src/models/attachment.py
- src/schemas/attachment.py
- tests/test_upload_attachment.py

Out of scope:
- Frontend upload UI
- Cloud storage integration (use local filesystem for now)
- File virus scanning
- Image thumbnail generation

---

## TASK-004: Implement permission check middleware for attachment operations

Context:
Attachment operations (upload, delete, print) require permission control. The system should enforce that only users with the correct permission can perform protected operations.

Goal:
Implement a permission check middleware that validates user permissions before allowing attachment operations.

Requirements:
- Extract user permissions from the authentication token or session.
- Validate required permission against the endpoint's permission_required annotation.
- Return 403 Forbidden if the user lacks the required permission.
- Return 401 Unauthorized if no authentication token is provided.
- Do NOT block read-only operations (preview, download, list) unless explicitly configured.

Acceptance Criteria:
- Authorized users can perform protected operations.
- Unauthorized users receive 403 with a clear error message.
- Unauthenticated users receive 401 with a clear error message.
- Read-only operations (preview, download) are accessible to authenticated users without special permissions.
- Permission checks are applied consistently across all attachment endpoints.

Testing:
- Add pytest test for authorized user access.
- Add pytest test for unauthorized user (403).
- Add pytest test for unauthenticated user (401).
- Add pytest test for read-only access without special permissions.

Instructions for AI Coding Agent:
- Do not modify user authentication or login logic.
- Use a decorator-based approach (e.g., @require_permission('ATTACHMENT_DELETE')).
- Ensure middleware can be unit tested without a full HTTP server.
- Add tests before implementation.

Files to modify:
- src/auth/permissions.py
- src/middleware/auth.py
- src/routers/attachments.py (add decorators)
- tests/test_attachment_permission.py

Out of scope:
- User role management UI
- Login/registration flow
- OAuth integration
- Password reset
