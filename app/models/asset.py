from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class AssetModel(Base):
    __tablename__ = "assets"

    no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    tracking_code = Column(String(50), unique=True, index=True, nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    start_date = Column(Date)
    users_name = Column(String(100))
