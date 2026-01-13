from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_by_org(self, organization_id: int):
        stmt = select(Project).where(
            Project.organization_id == organization_id
        )
        return self.session.scalars(stmt).all()

    def get(self, project_id: int, organization_id: int):
        stmt = select(Project).where(
            Project.id == project_id,
            Project.organization_id == organization_id,
        )

        return self.session.scalar(stmt)
    
    def create(self, name: str, organization_id: int):
        project = Project(
            name=name,
            organization_id=organization_id
        )
        self.session.add(project)
        self.session.flush()
        return project