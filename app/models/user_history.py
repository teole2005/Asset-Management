from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone


class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("MF_IT_Assets.id"), nullable=False, index=True)
    user_name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    assigned_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    returned_date = Column(DateTime, nullable=True)
    assigned_by = Column(String, nullable=False)
