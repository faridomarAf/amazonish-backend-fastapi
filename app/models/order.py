from sqlalchemy import BigInteger, ForeignKey, Integer, String, DECIMAL, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customers.id", ondelete="RESTRICT"), index=True
    )
    status: Mapped[str] = mapped_column(
        String(32), index=True)  # CREATED/PAID/etc
    total_amount: Mapped[str] = mapped_column(DECIMAL(19, 4))
    total_currency: Mapped[str] = mapped_column(String(3))

    shipping_address_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("customer_addresses.id", ondelete="SET NULL"), nullable=True
    )
    billing_address_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("customer_addresses.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"), onupdate=text("CURRENT_TIMESTAMP(6)")
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    sku_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("skus.id", ondelete="RESTRICT"), index=True
    )
    qty: Mapped[int] = mapped_column(Integer)
    unit_amount: Mapped[str] = mapped_column(DECIMAL(19, 4))
    unit_currency: Mapped[str] = mapped_column(String(3))

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
