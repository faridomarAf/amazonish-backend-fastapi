from sqlalchemy import BigInteger, DateTime, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

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

    created_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
    published_at: Mapped[str | None] = mapped_column(
        DateTime(fsp=6), nullable=True)
    publish_attempts: Mapped[int] = mapped_column(BigInteger, default=0)


class EventInbox(Base):
    __tablename__ = "event_inbox"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(36))
    consumer: Mapped[str] = mapped_column(String(64))

    received_at: Mapped[str] = mapped_column(
        DateTime(fsp=6), server_default=func.now())
