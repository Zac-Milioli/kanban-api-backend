"Funções para testes"

from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from db.database import project_database, client_database, activity_database
from src.schemas.project_schema import ProjectDB
from src.schemas.client_schema import ClientDB
from src.schemas.activity_schema import ActivityDB
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

@pytest.fixture()
def client_instance(project: ProjectDB):
    "Cria e retorna um client diretamente no banco"
    client_db = ClientDB(
        name="testClient",
        project_id=project.id,
        id=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
        )
    client_database[1] = client_db
    yield client_db
    if client_database.get(1):
        del client_database[1]

@pytest.fixture()
def activity(client_instance: ClientDB):
    "Cria e retorna uma activity diretamente no banco"
    activity_db = ActivityDB(
        name="testActivity",
        client_id=client_instance.id,
        id=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
        )
    activity_database[1] = activity_db
    yield activity_db
    if activity_database.get(1):
        del activity_database[1]
