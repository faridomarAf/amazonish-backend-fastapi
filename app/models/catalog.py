from sqlalchemy import BigInteger, ForeignKey, String, Text, DECIMAL, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", index=True)

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"), onupdate=text("CURRENT_TIMESTAMP(6)")
    )


class Sku(Base):
    __tablename__ = "skus"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.id", ondelete="RESTRICT"), index=True
    )
    sku_code: Mapped[str] = mapped_column(String(64), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    price_amount: Mapped[str] = mapped_column(DECIMAL(19, 4))
    price_currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", index=True)

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"), onupdate=text("CURRENT_TIMESTAMP(6)")
    )
