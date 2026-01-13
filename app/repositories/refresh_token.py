from sqlalchemy.orm import Session
from datetime import datetime

from app.models.refresh_token import RefreshToken

from app.core.security import hash_token, verify_token

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self, 
            user_id: int, 
            token_hash: str, 
            expires_at: datetime,
        ):
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.db.add(token)
        return token
    
    def get_by_token(self, token_raw: str) -> RefreshToken | None:
        tokens = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.revoked_at.is_(None))
            .filter(RefreshToken.expires_at > datetime.utcnow())
            .all()
        )

        for token in tokens:
            if verify_token(token_raw, token.token_hash):
                return token
            
        return None
    
    def revoke(self, token: RefreshToken):
        token.revoked_at = datetime.utcnow()