from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_session
from app.repositories.membership import MembershipRepository


def get_current_membership(
        organization_id: int,
        user = Depends(get_current_user),
        session = Depends(get_session)
):
    membership = MembershipRepository(session).get(
        user_id=user,
        organization_id=organization_id,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )
    
    return membership