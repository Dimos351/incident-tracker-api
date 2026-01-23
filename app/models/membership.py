from sqlalchemy import (
    ForeignKey,
    String, 
    UniqueConstraint,
    Index
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(String(50), nullable=False)

    user = relationship("User", back_populates="memberships",)
    organization = relationship("Organization", back_populates="memberships",)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            name="uq_user_org_membership",
        ),
        Index(
            "ix_membership_org_user",
            "organization_id",
            "user_id",
        )
    )
