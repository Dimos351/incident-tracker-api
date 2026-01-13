from app.core.permissions import require_role
from app.repositories.comment import CommentRepository
from app.repositories.incident import IncidentRepository


class CommentService:
    def __init__(self, session):
        self.comments = CommentRepository(session)
        self.incidents = IncidentRepository(session)

    def add_comment(self, membership, incident_id: int, body: str):
        require_role(membership, {"owner", "admin", "manager", "member"})

        incident = self.incidents.get(
            incident_id=incident_id,
            organization_id=membership.organization_id,
        )

        if not incident:
            return None
        
        return self.comments.create(
            incident_id=incident.id,
            author_id=membership.user_id,
            body=body,
        )
    
    def list_comments(self, membership, incident_id: int, limit: int, offset: int):
        incident = self.incidents.get(
            incident_id=incident_id,
            organization_id=membership.organization_id,
        )

        if not incident:
            return None

        return self.comments.list_by_incident(
            incident_id=incident.id,
            limit=limit,
            offset=offset,
        )



