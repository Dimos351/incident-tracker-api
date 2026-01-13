from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.organization import get_current_membership
from app.dependencies.db import get_session
from app.schemas.incident import IncidentCreate, IncidentRead
from app.services.incident import IncidentService

router = APIRouter(prefix="/organizations/{organization_id}/incidents")

@router.post("/", response_model=IncidentRead)
def create_incident(
    organization_id: int,
    data: IncidentCreate,
    membership = Depends(get_current_membership),
    session = Depends(get_session),
):
    service = IncidentService(session)
    incident = service.create(membership, data)

    if not incident:
        raise HTTPException(status_code=404, detail="Project not found")

    return incident