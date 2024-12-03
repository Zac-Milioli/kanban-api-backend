"Registro do model para client"

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from .table_registry import table_registry


@table_registry.mapped_as_dataclass
class ClientModel:
    "Modelo para Client"
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), init=True)
    name: Mapped[str] = mapped_column(init=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
