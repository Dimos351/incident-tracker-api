from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.organization import get_current_membership
from app.dependencies.db import get_session
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment import CommentService

router = APIRouter()

@router.post("")
def add_comment(
    organization_id: int,
    incident_id: int,
    data: CommentCreate,
    membership = Depends(get_current_membership),
    session: Session = Depends(get_session),
):
    if organization_id != membership.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization ID does not match your membership",
        )
    
    service = CommentService(session)
    comment = service.add_comment(membership, incident_id, data.body)

    if not comment:
        raise HTTPException(status_code=404, detail="Incident not found")

    return comment

@router.get("")
def list_comments(
    organization_id: int,
    incident_id: int,
    limit: int = 20,
    offset: int = 0,
    membership = Depends(get_current_membership),
    session = Depends(get_session),
):
    if organization_id != membership.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization ID does not match your membership",
        )

    service = CommentService(session)
    comments = service.list_comments(membership, incident_id, limit, offset)

    if comments is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return comments
