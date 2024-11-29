"Registro do model para project"

from datetime import datetime
from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func

table_registry = registry()

@table_registry.mapped_as_dataclass
class ProjectModel:
    "Modelo para Project"
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(init=True, unique=True)
    status: Mapped[str] = mapped_column(init=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False,
                                                    server_default=func.now(), onupdate=func.now())
