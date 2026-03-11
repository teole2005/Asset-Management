from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.asset import MFITAsset

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/")
def list_assets(
    search: str = "",
    status: str = "",
    type: str = "",
    db: Session = Depends(get_db),
):
    """Return all assets, optionally filtered by search, status, or type."""
    query = db.query(MFITAsset)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            MFITAsset.tracking_code.ilike(pattern)
            | MFITAsset.users_name.ilike(pattern)
            | MFITAsset.brand.ilike(pattern)
            | MFITAsset.model.ilike(pattern)
            | MFITAsset.serial_no.ilike(pattern)
            | MFITAsset.department.ilike(pattern)
        )

    if status:
        query = query.filter(MFITAsset.assignment_status == status)

    if type:
        query = query.filter(MFITAsset.type == type)

    assets = query.order_by(MFITAsset.id).all()

    return [
        {
            "id": a.id,
            "no": a.no,
            "type": a.type,
            "tracking_code": a.tracking_code,
            "brand": a.brand,
            "model": a.model,
            "serial_no": a.serial_no,
            "assignment_status": a.assignment_status,
            "users_name": a.users_name,
            "department": a.department,
        }
        for a in assets
    ]


@router.get("/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Return full details for a single asset by its database ID."""
    asset = db.query(MFITAsset).filter(MFITAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return {c.name: getattr(asset, c.name) for c in MFITAsset.__table__.columns}