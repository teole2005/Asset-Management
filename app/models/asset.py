from sqlalchemy import Column, Integer, String
from app.core.database import Base


class MFITAsset(Base):
    __tablename__ = "MF_IT_Assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    no = Column(String)
    type = Column(String)
    owner = Column(String)
    tracking_code = Column(String, unique=True, index=True)
    brand = Column(String)
    model = Column(String)
    serial_no = Column(String)
    cpu = Column(String)
    ram = Column(String)
    storage = Column(String)
    printer_type = Column(String)
    printer_color = Column(String)
    connectivity = Column(String)
    function = Column(String)
    monitor_size = Column(String)
    input_type = Column(String)
    price = Column(String)
    purchase_date = Column(String)
    estimate_lifespan = Column(String)
    expiry_date = Column(String)
    start_date = Column(String)
    used_years = Column(String)
    end_date = Column(String)
    assignment_status = Column(String)
    users_name = Column(String)
    department = Column(String)
    assignment_date = Column(String)
