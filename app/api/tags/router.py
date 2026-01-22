from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_session
from app.dependencies.organization import get_current_membership
from app.schemas.tag import TagRead
from app.services.tag import TagService, PermissionDeniedError


router = APIRouter()


@router.get("", response_model=list[TagRead], status_code=status.HTTP_200_OK)
def list_tags(
    membership = Depends(get_current_membership),
    session: Session = Depends(get_session),
):
    service = TagService(session)
    tags = service.list_tags(membership)
    
    try:
        return service.list_tags(membership)
    except PermissionDeniedError:
        raise HTTPException(
            status_code=403,
            detail="Permission denieds"
        )