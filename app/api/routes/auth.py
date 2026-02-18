from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Customer
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(request: RegisterRequest):
    with SessionLocal() as db:

        existing_user = db.scalar(
            select(Customer).where(Customer.email == request.email)
        )

        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        user = Customer(
            email=request.email,
            hashed_password=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            status="ACTIVE",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    with SessionLocal() as db:

        user = db.scalar(
            select(Customer).where(Customer.email == request.email)
        )

        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token({"sub": str(user.id)})

        return TokenResponse(access_token=access_token)
