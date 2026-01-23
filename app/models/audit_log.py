from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(String(100), nullable=False)

    entity: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(nullable=True)

    metadata: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

