from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.attachment import Attachment
from app.models.asset import MFITAsset
from app.api.auth import get_current_user
from app.models.auth import User
from fastapi.responses import FileResponse
import os
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["Attachments"])

# Upload directory (relative to project root)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/assets/{asset_id}/attachments")
def list_attachments(
    asset_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all attachments for an asset."""
    attachments = (
        db.query(Attachment)
        .filter(Attachment.asset_id == asset_id)
        .order_by(Attachment.upload_date.desc())
        .all()
    )
    return [
        {
            "id": a.id,
            "asset_id": a.asset_id,
            "original_name": a.original_name,
            "file_size": a.file_size,
            "upload_date": a.upload_date.isoformat() if a.upload_date else None,
            "uploaded_by": a.uploaded_by,
        }
        for a in attachments
    ]


@router.post("/assets/{asset_id}/attachments")
async def upload_attachment(
    asset_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Upload a file attachment for an asset."""
    # Verify asset exists
    asset = db.query(MFITAsset).filter(MFITAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Create asset-specific upload directory
    asset_dir = os.path.join(UPLOAD_DIR, str(asset_id))
    os.makedirs(asset_dir, exist_ok=True)

    # Generate unique filename
    ext = os.path.splitext(file.filename or "file")[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(asset_dir, stored_name)

    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Create DB record
    attachment = Attachment(
        asset_id=asset_id,
        filename=stored_name,
        original_name=file.filename or "unnamed",
        file_size=len(content),
        uploaded_by=user.display_name,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return {
        "id": attachment.id,
        "original_name": attachment.original_name,
        "file_size": attachment.file_size,
        "upload_date": attachment.upload_date.isoformat() if attachment.upload_date else None,
        "uploaded_by": attachment.uploaded_by,
    }


@router.get("/attachments/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Download an attachment file."""
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    file_path = os.path.join(UPLOAD_DIR, str(attachment.asset_id), attachment.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=attachment.original_name,
        media_type="application/octet-stream",
    )


@router.delete("/attachments/{attachment_id}")
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete an attachment."""
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    # Delete file from disk
    file_path = os.path.join(UPLOAD_DIR, str(attachment.asset_id), attachment.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(attachment)
    db.commit()

    return {"message": "Attachment deleted"}
