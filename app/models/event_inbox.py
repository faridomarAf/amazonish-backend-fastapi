from sqlalchemy import Column, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime
from app.db.base import Base


class EventInbox(Base):
    __tablename__ = "event_inbox"

    event_id = Column(String(36), primary_key=True)
    processed_at = Mapped[datetime] = mapped_column(
        DATETIME(fsp=6), server_default=text("CURRENT_TIMESTAMP(6)"))
