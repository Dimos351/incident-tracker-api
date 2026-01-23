from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_session
from app.services.auth import AuthService, UserAlreadyExistsError
from app.schemas.user import (
    UserCreate,
    UserRead,
    LoginRequest,
    TokenRead,
    RefreshRequest,
)


router = APIRouter()

# -------------------------
# Register
# -------------------------
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    data: UserCreate,
    session: Session = Depends(get_session)
):
    service = AuthService(session)
    
    try:
        user = service.register_user(data)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exsists",
        )
    
    return user


# -------------------------
# Login
# -------------------------
@router.post("/login", response_model=TokenRead)
def login_user(
    data: LoginRequest,
    session: Session = Depends(get_session),
):
    service = AuthService(session)

    try:
        access_token, refresh_token = service.login(
            email=data.email,
            password=data.password,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    return TokenRead(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# -------------------------
# Refresh
# -------------------------
@router.post("/refresh", response_model=TokenRead)
def refresh_tokens(
    data: RefreshRequest,
    session: Session = Depends(get_session),
):
    service = AuthService(session)

    try:
        access_token, refresh_token = service.refresh(data.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
    return TokenRead(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# -------------------------
# Logout
# -------------------------
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    data: RefreshRequest,
    session: Session = Depends(get_session),
):
    service = AuthService(session)

    try:
        service.logout(data.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    return None