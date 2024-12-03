"Setup para testes"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import src.models
from src.models.table_registry import table_registry
from src.models.project_model import ProjectModel
from src.models.client_model import ClientModel
from src.models.activity_model import ActivityModel
from src.utils.settings import Settings
from db.database import project_database, client_database, activity_database
from src.utils.database import get_session
from main import app

@pytest.fixture(scope="function")
def session():
    "Inicia uma sessão de testes"
    engine = create_engine(
        Settings().TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session_connection:
        yield session_connection

    table_registry.metadata.drop_all(engine)

@pytest.fixture()
def client(session: Session):
    "Retorna o cliente de testes"
    def get_session_override():
        return session

    with TestClient(app=app) as test_client:
        app.dependency_overrides[get_session] = get_session_override
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture()
def project(session: Session):
    "Cria e retorna um project diretamente no banco"
    project_db = ProjectModel(
        name="testProject",
        status="testStatus",
        )
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project_db

@pytest.fixture()
def client_instance(project: ProjectModel, session: Session):
    "Cria e retorna um client diretamente no banco"
    client_db = ClientModel(
        name="testClient",
        project_id=project.id,
        )
    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return client_db

@pytest.fixture()
def activity(client_instance: ClientModel, session: Session):
    "Cria e retorna uma activity diretamente no banco"
    activity_db = ActivityModel(
        name="testActivity",
        client_id=client_instance.id,
        status="testStatus",
        )
    session.add(activity_db)
    session.commit()
    session.refresh(activity_db)
    return activity_db
