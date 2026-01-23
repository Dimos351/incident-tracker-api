from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRead, UserUpdate


router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.put("/me", response_model=UserRead)
def update_me(
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repo = UserRepository(session)
    user = repo.update(current_user.id, **data.dict(exclude_unset=True))
    return user