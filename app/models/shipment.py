from sqlalchemy import Column, BigInteger, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime
from app.db.base import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id"))
    status = Column(String(50), default="CREATED")
    carrier = Column(String(100))
    tracking_number = Column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
