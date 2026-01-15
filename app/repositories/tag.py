from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, organization_id: int, name: int) -> Tag:
        stmt = select(Tag).where(
            Tag.organization_id == organization_id,
            Tag.name == name,
        )
        tag = self.session.scalar(stmt)

        if tag: 
            return tag
        
        tag = Tag(
            organization_id=organization_id,
            name=name,
        )

        self.session.add(tag)
        self.session.flush()
        return tag
        