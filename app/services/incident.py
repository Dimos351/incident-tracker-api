from app.core.permissions import require_role
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.repositories.project import ProjectRepository


class IncidentService:
    def __init__(self, session):
        self.incidents = IncidentRepository(session)
        self.projects = ProjectRepository(session)

    def create(self, membership, data):
        require_role(membership, {"owner", "admin", "manager"})

        project = self.projects.get(
            project_id=data.project_id,
            organization_id=membership.organization_id,
        )

        if not project:
            return None
        
        incident = Incident(
            organization_id=membership.organization_id,
            project_id=project.id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            created_by_id=membership.user_id,
        )

        return self.incidents.create(incident)
    
    def list_by_project(
        self,
        membership,
        project_id: int,
        limit: int,
        offset: int,
    ):
        project = self.projects.get(
            project_id=project_id,
            organization_id=membership.organization_id,
        )

        if not project:
            return None

        return self.incidents.list_by_project(
            organization_id=membership.organization_id,
            project_id=project_id,
            limit=limit,
            offset=offset,
        )
