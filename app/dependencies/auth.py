from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.jwt import decode_access_token
from app.dependencies.db import get_session
from app.api.auth.dependencies import get_bearer_token
from app.repositories.user import UserRepository

def get_current_user(
    token: str = Depends(get_bearer_token),
    session: Session = Depends(get_session),
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = UserRepository(session).get_by_id(int(user_id))

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user
