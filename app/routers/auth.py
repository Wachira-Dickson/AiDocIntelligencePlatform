from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import (
    authenticate_user,
    create_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    
    user = create_user(
        db=db,
        email=email,
        password=password,
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }

@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=email,
        password=password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }