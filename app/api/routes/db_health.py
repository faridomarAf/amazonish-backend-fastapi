from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal

router = APIRouter()


@router.get("/health/db")
def db_health():
    # Open a DB session and run a tiny query
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"db": "ok"}
