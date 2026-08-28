from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database_config import Base

if TYPE_CHECKING:
    from app.models.task_model import Task
    from app.models.user_model import User


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
