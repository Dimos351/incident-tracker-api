from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token import RefreshTokenRepository

from app.core.jwt import create_access_token
from app.core.security import generate_refresh_token, hash_password, verify_password, hash_token
from app.core.config import settings
from jose import jwt


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.refresh_repo = RefreshTokenRepository(self.db)


    def register_user(self, email: str, password: str) -> User:
        user = User(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user


    def login(self, user: User) -> tuple[str, str]:
        access_token = create_access_token(user.id)

        refresh_token = generate_refresh_token()
        refresh_token_hash = hash_token(refresh_token)

        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        self.refresh_repo.create(user.id, refresh_token_hash, refresh_token)

        self.db.commit()

        return access_token, refresh_token


    def refresh(self, refresh_token: str) -> tuple[str, str]:

        token = self._get_valid_refresh_token(refresh_token)

        token.revoked_at = datetime.utcnow()

        new_refresh_token = generate_refresh_token()
        new_refresh_token_hash = hash_token(new_refresh_token)

        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        self.db.add(
            RefreshToken(
                user_id=token.user_id,
                token_hash=new_refresh_token_hash,
                expires_at=expires_at
            )
        )

        self.db.commit()

        access_token = create_access_token(token.user_id)

        return access_token, new_refresh_token
    
    
    def logout(self, refresh_token: str) -> None:
        token = self._get_valid_refresh_token(token)

        token.revoked_at = datetime.utcnow()
        self.db.commit()


    def _get_valid_refresh_token(self, refresh_token: str) -> RefreshToken:
        token_obj = self.refresh_repo.get_by_token(refresh_token)
        if not token_obj:
            raise Exception("Invalid refresh token")
        if token_obj.revoked_at is not None:
            raise Exception("Token revoked")
        if token_obj.expires_at < datetime.utcnow():
            raise Exception("Token expired")
        return

