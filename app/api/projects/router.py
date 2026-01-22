from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_session
from app.dependencies.organization import get_current_membership
from app.schemas.project import (
    ProjectCreate, 
    ProjectRead, 
    ProjectUpdate,
)
from app.services.project import ProjectService, ProjectNotFound



router = APIRouter()


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    membership = Depends(get_current_membership),
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.create(membership, data.name)


@router.get("", response_model=List[ProjectRead], status_code=status.HTTP_200_OK)
def list_project(
    membership = Depends(get_current_membership),
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    return service.list(membership)


@router.get("/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def get_project(
    project_id: int,
    membership = Depends(get_current_membership),
    session: Session = Depends(get_session),
):
    service = ProjectService(session)
    try:
        project = service.get(membership, project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.patch("/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    membership = Depends(get_current_membership),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)
    try:
        project = service.update(
            membership,
            project_id,
            name=data.name,
        )
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    membership = Depends(get_current_membership),
    db: Session = Depends(get_session),
):
    service = ProjectService(db)
    try:
        service.delete(membership, project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
