from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

app = FastAPI(title="Attachment Management API", version="1.0.0")

# In-memory storage for demo
attachments_db = {}
audit_logs_db = []

# Mock permission database
USER_PERMISSIONS = {
    "user_1": ["ATTACHMENT_UPLOAD", "ATTACHMENT_PREVIEW", "ATTACHMENT_DOWNLOAD", "ATTACHMENT_PRINT", "ATTACHMENT_DELETE", "ATTACHMENT_LIST"],
    "user_2": ["ATTACHMENT_PREVIEW", "ATTACHMENT_DOWNLOAD", "ATTACHMENT_LIST"],  # No upload/delete
}

class AttachmentResponse(BaseModel):
    attachment_id: str
    file_name: str
    status: str

class AttachmentListResponse(BaseModel):
    items: list
    total: int
    status: str

class AuditLogEntry(BaseModel):
    user_id: str
    action: str
    attachment_id: Optional[str] = None
    timestamp: str
    details: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str
    message: str


def get_current_user():
    # Mock authentication - in production, use OAuth2/JWT
    return {"user_id": "user_1", "permissions": USER_PERMISSIONS.get("user_1", [])}


def check_permission(user: dict, permission: str):
    if permission not in user.get("permissions", []):
        raise HTTPException(status_code=403, detail=f"Permission denied: {permission} required")


def log_audit(user_id: str, action: str, attachment_id: Optional[str] = None, details: Optional[str] = None):
    audit_logs_db.append({
        "user_id": user_id,
        "action": action,
        "attachment_id": attachment_id,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details,
    })


@app.post("/api/attachments", response_model=AttachmentResponse)
async def upload_attachment(
    file: UploadFile = File(...),
    business_object_type: str = Form(...),
    business_object_id: str = Form(...),
    user: dict = Depends(get_current_user),
):
    check_permission(user, "ATTACHMENT_UPLOAD")

    attachment_id = str(uuid.uuid4())
    attachment = {
        "attachment_id": attachment_id,
        "file_name": file.filename,
        "business_object_type": business_object_type,
        "business_object_id": business_object_id,
        "content_type": file.content_type,
        "size": 0,  # Would read actual size in production
        "created_at": datetime.utcnow().isoformat(),
    }
    attachments_db[attachment_id] = attachment

    log_audit(user["user_id"], "UPLOAD", attachment_id, f"Uploaded {file.filename}")

    return AttachmentResponse(
        attachment_id=attachment_id,
        file_name=file.filename,
        status="success",
    )


@app.get("/api/attachments/{attachment_id}/preview")
async def preview_attachment(attachment_id: str, user: dict = Depends(get_current_user)):
    check_permission(user, "ATTACHMENT_PREVIEW")

    if attachment_id not in attachments_db:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment = attachments_db[attachment_id]
    log_audit(user["user_id"], "PREVIEW", attachment_id)

    return {
        "preview_url": f"/api/attachments/{attachment_id}/content",
        "status": "success",
    }


@app.get("/api/attachments/{attachment_id}/download")
async def download_attachment(attachment_id: str, user: dict = Depends(get_current_user)):
    check_permission(user, "ATTACHMENT_DOWNLOAD")

    if attachment_id not in attachments_db:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment = attachments_db[attachment_id]
    log_audit(user["user_id"], "DOWNLOAD", attachment_id)

    return {
        "download_url": f"/api/attachments/{attachment_id}/content",
        "status": "success",
    }


@app.get("/api/attachments/{attachment_id}/print")
async def print_attachment(attachment_id: str, user: dict = Depends(get_current_user)):
    check_permission(user, "ATTACHMENT_PRINT")

    if attachment_id not in attachments_db:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment = attachments_db[attachment_id]
    log_audit(user["user_id"], "PRINT", attachment_id)

    return {
        "print_url": f"/api/attachments/{attachment_id}/content?format=print",
        "status": "success",
    }


@app.delete("/api/attachments/{attachment_id}")
async def delete_attachment(attachment_id: str, user: dict = Depends(get_current_user)):
    check_permission(user, "ATTACHMENT_DELETE")

    if attachment_id not in attachments_db:
        raise HTTPException(status_code=404, detail="Attachment not found")

    attachment = attachments_db.pop(attachment_id)
    log_audit(user["user_id"], "DELETE", attachment_id, f"Deleted {attachment['file_name']}")

    return {"status": "success", "message": "Attachment deleted"}


@app.get("/api/attachments")
async def list_attachments(
    business_object_type: Optional[str] = None,
    business_object_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    user: dict = Depends(get_current_user),
):
    check_permission(user, "ATTACHMENT_LIST")

    items = list(attachments_db.values())

    if business_object_type:
        items = [a for a in items if a["business_object_type"] == business_object_type]
    if business_object_id:
        items = [a for a in items if a["business_object_id"] == business_object_id]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]

    log_audit(user["user_id"], "LIST", details=f"Listed {len(paginated_items)} attachments")

    return {
        "items": paginated_items,
        "total": total,
        "status": "success",
    }


@app.get("/api/audit-logs")
async def get_audit_logs(user: dict = Depends(get_current_user)):
    # Only admins can view all audit logs
    check_permission(user, "ATTACHMENT_LIST")
    return {"logs": audit_logs_db, "status": "success"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
