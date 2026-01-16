from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.scalar(stmt)
    
    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)
    
    def update(self, user_id: int, **fields) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        for key, value in fields.items():
            setattr(user, key, value)

        self.session.add(user)
        self.session.flush()
        return user