from datetime import datetime, date
from sqlalchemy import ForeignKey, String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class TaskStatus(str, enum.Enum):
    todo = "todo"
    is_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.todo,
        nullable=False,
    )

    due_date: Mapped[date | None] = mapped_column(Date)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")