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
        return org