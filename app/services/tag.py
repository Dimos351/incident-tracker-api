from app.core.permissions import require_role
from app.repositories.tag import TagRepository


class PermissionDeniedError(Exception):
    pass


class TagService:
    def __init__(self, session):
        self.tags = TagRepository(session)

    def list_tags(self, membership):
        return self.tags.list_by_organization(organization_id=membership.organization_id)