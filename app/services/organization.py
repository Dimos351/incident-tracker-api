from app.models.membership import Membership
from app.repositories.organization import OrganizationRepository
from app.repositories.membership import MembershipRepository


class OrganizationService:
    def __init__(self, org_repo: OrganizationRepository, membership_repo: MembershipRepository):
        self.org_repo = org_repo
        self.membership_repo = membership_repo

    def create_with_owner(self, *, user_id: int, name: str,):
        org = self.org_repo.create(name)

        self.membership_repo.create(
            organization_id=org.id,
            user_id=user_id,
            role="owner",
        )

        return org
    
    def list_user_organizations(self, user_id: int):
        return self.membership_repo.list_organizations_for_user(user_id)
    
    def get_user_organization(self, org_id: int, user_id: int):
        return self.membership_repo.get_organizations_for_user(org_id, user_id)