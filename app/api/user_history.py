from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user_history import UserHistory
from app.api.auth import get_current_user
from app.models.auth import User

router = APIRouter(tags=["UserHistory"])


@router.get("/assets/{asset_id}/user-history")
def get_user_history(
    asset_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Return all user assignment history for an asset, newest first."""
    entries = (
        db.query(UserHistory)
        .filter(UserHistory.asset_id == asset_id)
        .order_by(UserHistory.assigned_date.desc())
        .all()
    )
    return [
        {
            "id": e.id,
            "asset_id": e.asset_id,
            "user_name": e.user_name,
            "department": e.department,
            "assigned_date": e.assigned_date.isoformat() if e.assigned_date else None,
            "returned_date": e.returned_date.isoformat() if e.returned_date else None,
            "assigned_by": e.assigned_by,
        }
        for e in entries
    ]
