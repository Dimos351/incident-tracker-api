from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.organization import get_current_membership
from app.dependencies.db import get_session
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment import CommentService

router = APIRouter(
    prefix="/organizations/{organization_id}/incidents/{incident_id}/comments",
    tags=["comments"],
)

@router.post("/")
def add_comment(
    organization_id: int,
    incident_id: int,
    data: CommentCreate,
    membership = Depends(get_current_membership),
    session = Depends(get_session),
):
    service = CommentService(session)
    comment = service.add_comment(membership, incident_id, data.body)

    if not comment:
        raise HTTPException(status_code=404, detail="Incident not found")

    return comment

@router.get("/")
def list_comments(
    organization_id: int,
    incident_id: int,
    limit: int = 20,
    offset: int = 0,
    membership = Depends(get_current_membership),
    session = Depends(get_session),
):
    service = CommentService(session)
    comments = service.list_comments(membership, incident_id, limit, offset)

    if comments is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return comments
