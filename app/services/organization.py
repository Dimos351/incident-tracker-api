from app.models.membership import Membership
from app.repositories.organization import OrganizationRepository


class OrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def create_with_owner(self, *, user_id: int, name: str,):
        org = self.repo.create(name)

        self.repo.add_member(
            organization_id=org.id,
            user_id=user_id,
            role="owner",
        )

        return org
    
    def list_user_organizations(self, user_id: int):
        return self.repo.list_for_user(user_id)
    
    def get_user_organization(self, org_id: int, user_id: int):
        return self.repo.get_for_user(org_id, user_id)