from Application import db
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, null


class Todo(db.Model): # type: ignore
    id: Mapped[int] = mapped_column(primary_key=True, init=False, repr=True)
    title: Mapped[str] = mapped_column(String(24), init=True, nullable=False, repr=True)
    description: Mapped[str] = mapped_column(String(512), init=True, nullable=False, repr=True)
    imagename: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, repr=True, default=null(),unique=True, init=False)