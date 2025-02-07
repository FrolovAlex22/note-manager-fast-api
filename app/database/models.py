from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        index=True, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        index=True, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(70), nullable=False)


    tasks: Mapped[Optional[list["Task"]]] = relationship(
        back_populates="members",
        secondary="user_task",
    )

    def __str__(self):
        return f"{self.username}"


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    members: Mapped[list["User"]] = relationship(
        back_populates="tasks",
        secondary="user_task",
    )


class UserTask(Base):
    __tablename__ = "user_task"


    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
    )

    def __str__(self):
        return f"{self.user_id} - {self.task_id}"
