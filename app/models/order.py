from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

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

    created_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now(), onupdate=func.now()
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

    created_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
