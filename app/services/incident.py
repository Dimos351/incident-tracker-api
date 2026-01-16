from app.core.permissions import require_role
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.repositories.project import ProjectRepository
from app.repositories.tag import TagRepository

class IncidentService:
    def __init__(self, session):
        self.incidents = IncidentRepository(session)
        self.projects = ProjectRepository(session)
        self.tags = TagRepository(session)

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
    
    def set_tags(self, membership, incident, tag_names: list[str]):
        require_role(membership, {"owner", "admin", "manager"})

        tags = []
        for name in tag_names:
            tag = self.tags.get_or_create(
                organization_id=membership.organization_id,
                name=name,
            )
            tags.append(tag)

        incident.tags = tags
