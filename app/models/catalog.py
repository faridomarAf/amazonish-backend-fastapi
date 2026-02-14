from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", index=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now(), onupdate=func.now()
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

    created_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now(), onupdate=func.now()
    )
