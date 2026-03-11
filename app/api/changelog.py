from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.changelog import ChangeLog
from app.api.auth import get_current_user
from app.models.auth import User

router = APIRouter(tags=["ChangeLog"])


@router.get("/assets/{asset_id}/changelog")
def get_changelog(
    asset_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Return all change log entries for an asset, newest first."""
    entries = (
        db.query(ChangeLog)
        .filter(ChangeLog.asset_id == asset_id)
        .order_by(ChangeLog.changed_at.desc())
        .all()
    )
    return [
        {
            "id": e.id,
            "asset_id": e.asset_id,
            "field_name": e.field_name,
            "old_value": e.old_value,
            "new_value": e.new_value,
            "changed_by": e.changed_by,
            "changed_at": e.changed_at.isoformat() if e.changed_at else None,
        }
        for e in entries
    ]
