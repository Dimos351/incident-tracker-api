from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.models.organization import Organization

class MembershipRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
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

    def get(self, user_id: int, organization_id: int) -> Membership | None:
        stmt = select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == organization_id,
        )
        return self.session.scalar(stmt)
    
    def list_organizations_for_user(self, user_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Membership)
            .where(Membership.user_id == user_id)
        )

        return self.session.execute(stmt).scalars().all()
    
    def get_organizations_for_user(self, org_id: int, user_id: int) -> Organization | None:
        stmt = (
            select(Organization)
            .join(Membership)
            .where(
                Organization.id == org_id,
                Membership.user_id == user_id,
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()
    

    