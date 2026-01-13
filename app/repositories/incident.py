from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incident import Incident


class IncidentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, incident: Incident) -> Incident:
        self.session.add(incident)
        self.session.flush()
        return incident

    def get(self, *, incident_id: int, organization_id: int) -> Incident | None:
        stmt = (
            select(Incident)
            .where(
                Incident.id == incident_id,
                Incident.organization_id == organization_id,
            )
        )
        return self.session.scalar(stmt)

    def list_by_project(
        self,
        *,
        organization_id: int,
        project_id: int,
        limit: int,
        offset: int,
    ):
        stmt = (
            select(Incident)
            .where(
                Incident.organization_id == organization_id,
                Incident.project_id == project_id,
            )
            .order_by(Incident.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self.session.scalars(stmt).all()
   