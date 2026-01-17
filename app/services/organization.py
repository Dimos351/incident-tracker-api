from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.repositories.organization import OrganizationRepository


class OrganizationService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = OrganizationRepository(session)

    def create_with_owner(self, name: str, user_id: int):
        org = self.repo.create(name)

        membership = Membership(
            user_id=user_id,
            organization_id = org.id,
            role="owner",
        )

        self.session.add(membership)
        self.session.commit()
        return org
    
    def list_user_organizations(self, user_id: int):
        return self.repo.list_for_user(user_id)
    
    def get_user_organization(self, org_id: int, user_id: int):
        return self.repo.get_for_user(org_id, user_id)