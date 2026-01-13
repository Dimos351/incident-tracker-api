from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membership import Membership

class MembershipRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: int, organization_id: int) -> Membership | None:
        stmt = select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == organization_id,
        )
        return self.session.scalar(stmt)
    