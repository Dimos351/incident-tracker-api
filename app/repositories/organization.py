from sqlalchemy.orm import Session

from app.models.organization import Organization

class OrganizationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str) -> Organization:
        org = Organization(name=name)
        self.session.add(org)
        self.session.flush()
        return org
        
    def get_by_id(self, org_id: int) -> Organization | None:
        return self.session.get(Organization, org_id)