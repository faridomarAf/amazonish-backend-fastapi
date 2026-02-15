from sqlalchemy import BigInteger, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME

from app.db.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    sku_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("skus.id", ondelete="RESTRICT"), primary_key=True
    )
    on_hand: Mapped[int] = mapped_column(Integer, default=0)
    reserved: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[int] = mapped_column(BigInteger, default=0)

    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"), onupdate=text("CURRENT_TIMESTAMP(6)")
    )
