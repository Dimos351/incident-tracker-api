from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.organization import Organization
from app.models.membership import Membership

class OrganizationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str) -> Organization:
        org = Organization(name=name)
        self.session.add(org)
        self.session.flush()
        return org
    
    def add_member(
        self, 
        organization_id: int, 
        user_id: int,
        role: str,
    ) -> Membership:
        
        membership = Membership(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        self.session.add(membership)
        self.session.flush()
        return membership
        
    def get_by_id(self, org_id: int) -> Organization | None:
        return self.session.get(Organization, org_id)
    
    def list_for_user(self, user_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Membership)
            .where(Membership.user_id == user_id)
        )

        return self.session.execute(stmt).scalars().all()
    
    def get_for_user(self, org_id: int, user_id: int) -> Organization | None:
        stmt = (
            select(Organization)
            .join(Membership)
            .where(
                Organization.id == org_id,
                Membership.user_id == user_id,
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()