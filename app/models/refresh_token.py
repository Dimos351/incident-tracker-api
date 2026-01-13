from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash = Column(String, nullable=False, unique=True)

    expires_at = Column(DateTime, nullable=False)

    revoked_at = Column(DateTime, nullable=False)

    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False,
    )

    
    

