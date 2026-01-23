from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user 
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
)
from app.schemas.membership import MembershipRead
from app.services.organization import OrganizationService
from app.repositories.organization import OrganizationRepository
from app.repositories.membership import MembershipRepository 



router = APIRouter()


@router.post(
    "", 
    response_model=OrganizationCreate, 
    status_code=status.HTTP_201_CREATED
)
def create_organization(
    data: OrganizationCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    service = OrganizationService(
        org_repo=OrganizationRepository(session), 
        membership_repo=MembershipRepository(session)
    )
    org = service.create_with_owner(user_id=current_user.id, name=data.name)

    return org


@router.get(
    "",
    response_model=List[OrganizationRead]
)
def list_user_organization(
    user = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    service = OrganizationService(
        org_repo=OrganizationRepository(session), 
        membership_repo=MembershipRepository(session)
    )
    return service.list_user_organizations(user_id=user.id)


@router.get(
    "/{org_id}",
    response_model=OrganizationRead,
)
def get_user_organization(
    org_id: int,
    user = Depends(get_current_user),
    session: Session = Depends(get_session),
): 
    service = OrganizationService(
        org_repo=OrganizationRepository(session), 
        membership_repo=MembershipRepository(session)
    )
    org = service.get_user_organization(org_id=org_id, user_id=user.id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization"
        )
    return org

@router.get(
    "/{org_id}/members",
    response_model=List[OrganizationRead]
)
def list_organization_members(
    org_id: int,
    user = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    service = OrganizationService(
        org_repo=OrganizationRepository(session), 
        membership_repo=MembershipRepository(session)
    )
    org = service.list_user_organizations(org_id=org_id, user_id=user.id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization"
        )
    return [
        MembershipRead.model_validate(membership)
        for membership in org.memberships
    ]