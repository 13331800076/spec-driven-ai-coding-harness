# Acceptance Criteria

## US-001: Upload attachments

- Given a business user has ATTACHMENT_UPLOAD permission
- When the user selects a valid file and submits the upload form
- Then the file should be stored successfully
- And the file metadata should be linked to the business object
- And an audit log should be created

- Given a business user does not have ATTACHMENT_UPLOAD permission
- When the user attempts to upload an attachment
- Then the system should reject the operation
- And return a permission denied message
- And no file should be stored

- Given a business user provides an invalid file type
- When the user attempts to upload the file
- Then the system should validate the file type
- And return an appropriate error message
- And the operation should not proceed

- Given a business user successfully uploads a file
- When the upload operation completes
- Then the system should record an audit log
- And the log should include the user identifier
- And the log should include a timestamp of the operation

## US-005: Delete attachments

- Given a business user has ATTACHMENT_DELETE permission
- When the user selects an attachment and confirms deletion
- Then the attachment should be removed from the system
- And the file metadata should be updated
- And an audit log should be created

- Given a business user does not have ATTACHMENT_DELETE permission
- When the user attempts to delete an attachment
- Then the system should reject the operation
- And return a permission denied message
- And no attachment should be deleted

- Given a business user attempts to delete a non-existent attachment
- When the deletion request is submitted
- Then the system should return a 404 not found error
- And no changes should be made to the system
