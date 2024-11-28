"Funções para testes"

from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from db.database import project_database
from src.schemas.project_schema import ProjectDB
from main import app

@pytest.fixture()
def client():
    "Retorna o cliente de testes"
    return TestClient(app=app)

@pytest.fixture()
def project():
    "Cria e retorna um project diretamente no banco"
    project_db = ProjectDB(
        name="testProject",
        status="testStatus",
        id=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
        )
    project_database[1] = project_db
    yield project_db
    if project_database.get(1):
        del project_database[1]
