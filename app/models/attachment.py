from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("MF_IT_Assets.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)        # stored filename (uuid-based)
    original_name = Column(String, nullable=False)    # original upload name
    file_size = Column(Integer, default=0)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    uploaded_by = Column(String, nullable=False)
