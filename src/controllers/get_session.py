"Sessão usada nas requisições"

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import src.models
from src.models.table_registry import table_registry
from .settings import Settings

def get_session():
    "Retorna a sessão"
    engine = create_engine(Settings().DATABASE_URL)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
