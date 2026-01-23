from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_session
from app.dependencies.organization import get_current_membership
from app.schemas.incident import (
    IncidentCreate,
    IncidentRead,
    IncidentList,
)
from app.services.incident import IncidentService


router = APIRouter()

@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(
    project_id: int,
    data: IncidentCreate,
    session: Session = Depends(get_session),
    membership = Depends(get_current_membership),
):
    service = IncidentService(session)
    incident = service.create(membership, data)

    if not incident:
        raise HTTPException(status_code=404, detail="Project not found")
    
    session.commit()

    return incident

@router.get("", response_model=IncidentList)
def list_incidents(
    project_id: int,
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
    membership = Depends(get_current_membership),
):
    service = IncidentService(session)

    incidents = service.list_by_project(
        membership=membership,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )
    if incidents is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return {
        "items": incidents,
        "limit": limit,
        "offset": offset,
        "count": len(incidents),
    }

@router.post("/{incident_id}/tags", status_code=status.HTTP_204_NO_CONTENT)
def set_incident_tags(
    incident_id: int,
    tag_name: list[str],
    session: Session = Depends(get_session),
    membership = Depends(get_current_membership),
):
    service = IncidentService(session)

    incident = service.incidents.get(
        incident_id=incident_id,
        organization_id=membership.organization_id,
    )

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    
    service.set_tags(
        membership=membership,
        incident=incident,
        tag_names=tag_name,
    )
