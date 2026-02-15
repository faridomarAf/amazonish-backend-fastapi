from sqlalchemy import BigInteger, JSON, String, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME

from app.db.base import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)

    aggregate_type: Mapped[str] = mapped_column(String(64), index=True)
    aggregate_id: Mapped[int] = mapped_column(BigInteger, index=True)

    event_type: Mapped[str] = mapped_column(String(128))
    payload: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
    published_at: Mapped[datetime | None] = mapped_column(
        DATETIME(fsp=6), nullable=True)
    publish_attempts: Mapped[int] = mapped_column(BigInteger, default=0)


class EventInbox(Base):
    __tablename__ = "event_inbox"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(36))
    consumer: Mapped[str] = mapped_column(String(64))

    received_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
