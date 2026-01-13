from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment

class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, incident_id: int, author_id: int, body: str) -> Comment:
        comment = Comment(
            incident_id=incident_id,
            author_id=author_id,
            body=body,
        )
        self.session.add(comment)
        self.session.flush()
        return comment

    def list_by_incident(self, incident_id: int, limit: int, offset: int):
        stmt = (
            select(Comment)
            .where(Comment.incident_id == incident_id)
            .order_by(Comment.created_at)
            .limit(limit)
            .offset(offset)
        )

        return self.session.scalars(stmt).all()