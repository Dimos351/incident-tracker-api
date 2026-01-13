from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.dependencies.db import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, TokenRead
from app.services.auth import AuthService
from app.core.config import settings
from app.dependencies.auth import get_bearer_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    user = AuthService.register_user(session, user_data)
    return user


@router.post("/login", response_model=TokenRead)
def login_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    token = AuthService.login(
        session=session,
        username=user_data.username,
        password=user_data.password,
    )
    
    return token