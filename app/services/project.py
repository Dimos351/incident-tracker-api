from app.repositories.project import ProjectRepository
from app.core.permissions import require_role


class ProjectService:
    def __init__(self, session):
        self.repo = ProjectRepository(session)

    def create(self, membership, name: str):
        require_role(membership, {"owner", "admin", "manager"})

        return self.repo.create(
            name=name,
            organization_id=membership.organization_id,
        )
    
    def delete(self, membership, project_id: int):
        require_role(membership, {"owner", "admin"})

        project = self.repo.get(
            project_id=project_id,
            organization_id=membership.organization_id, 
        )

    def list(self, membership):
        return self.repo.list_by_org(membership.organization_id)
    
    