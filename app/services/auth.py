from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.user import UserRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.schemas.user import UserCreate

from app.core.jwt import create_access_token
from app.core.security import (
    generate_refresh_token,
    hash_password,
    verify_password,
    hash_token,
)
from app.core.config import settings


class UserAlreadyExistsError(Exception):
    pass

class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.users = UserRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)


    def register_user(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            is_active=True,
        )

        self.session.add(user)
        self.session.flush()    
        self.session.refresh(user)

        return user


    def login(self, email: str, password: str) -> tuple[str, str]:
        user = self.users.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        access_token = create_access_token(user.id)

        refresh_token = generate_refresh_token()
        refresh_token_hash = hash_token(refresh_token)

        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        self.refresh_repo.create(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
        
        return access_token, refresh_token


    def refresh(self, refresh_token: str) -> tuple[str, str]:

        token = self._get_valid_refresh_token(refresh_token)

        token.revoked_at = datetime.now(timezone.utc)

        new_refresh_token = generate_refresh_token()
        new_refresh_token_hash = hash_token(new_refresh_token)

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        self.refresh_repo.create(
            user_id=token.user_id,
            token_hash=new_refresh_token_hash,
            expires_at=expires_at
        )

        access_token = create_access_token(token.user_id)

        return access_token, new_refresh_token
    
    
    def logout(self, refresh_token: str) -> None:
        token = self._get_valid_refresh_token(refresh_token)
        token.revoked_at = datetime.now(timezone.utc)
        

    def _get_valid_refresh_token(self, refresh_token: str) -> RefreshToken:
        token_obj = self.refresh_repo.get_by_token(refresh_token)
        if not token_obj:
            raise ValueError("Invalid refresh token")
        if token_obj.revoked_at is not None:
            raise ValueError("Token revoked")
        if token_obj.expires_at < datetime.now(timezone.utc):
            raise ValueError("Token expired")
        return token_obj

