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
    # with TestClient(app=app) as test_client:
    #     yield test_client
    return TestClient(app=app)

@pytest.fixture()
def project():
    "Cria e retorna um project diretamente no banco"
    project_db = ProjectDB(
        name="testProject",
        id=len(project_database)+1,
        created_at=datetime.now(),
        updated_at=datetime.now()
        )
    project_database.append(project_db)
    return project_db
