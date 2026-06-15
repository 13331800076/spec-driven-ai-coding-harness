# Test Cases

## TC-001: Upload attachment successfully

Steps:
1. Login as a business user with ATTACHMENT_UPLOAD permission.
2. Open a business document (e.g., purchase order).
3. Click the upload button and select a valid PDF file.
4. Submit the upload form.

Expected Result:
- The upload succeeds with a 200 status code.
- The attachment appears in the attachment list.
- The audit log records the upload operation with user ID and timestamp.

## TC-002: Upload attachment without permission

Steps:
1. Login as a user without ATTACHMENT_UPLOAD permission.
2. Attempt to upload an attachment via API.
3. Submit the request.

Expected Result:
- The operation is rejected with a 403 status code.
- The response contains a permission denied message.
- No file is stored in the system.
- No audit log is created for the failed attempt.

## TC-003: Delete attachment with permission

Steps:
1. Login as a business user with ATTACHMENT_DELETE permission.
2. Open the attachment list for a business document.
3. Select an existing attachment and confirm deletion.
4. Submit the delete request.

Expected Result:
- The deletion succeeds with a 200 status code.
- The attachment is removed from the list.
- The audit log records the deletion operation.
- The file is removed from storage.

## TC-004: Delete attachment without permission

Steps:
1. Login as a user without ATTACHMENT_DELETE permission.
2. Open the attachment list.
3. Attempt to delete an attachment via API.

Expected Result:
- The operation is rejected with a 403 status code.
- The attachment remains unchanged.
- A permission denied message is returned.
- No audit log is created for the failed attempt.

## TC-005: Preview attachment

Steps:
1. Login as a user with ATTACHMENT_PREVIEW permission.
2. Open a business document with attachments.
3. Click the preview button for an attachment.

Expected Result:
- A preview is rendered in the browser or a preview URL is returned.
- The preview shows the correct file content.
- The audit log records the preview operation.

## TC-006: Download attachment

Steps:
1. Login as a user with ATTACHMENT_DOWNLOAD permission.
2. Open a business document with attachments.
3. Click the download button for an attachment.

Expected Result:
- The file is downloaded successfully.
- The downloaded file matches the original file content.
- The audit log records the download operation.
