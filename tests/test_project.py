"Testes para project"

from fastapi.testclient import TestClient
from src.schemas.project_schema import ProjectDB
from db.database import project_database

class TestProject:
    "Objeto de testes para project"
    def test_create_project(self, client: TestClient):
        "Testa a criação de um project"
        project = {
            "name": "testProject"
        }
        response = client.post("/project", json=project).json()
        assert response.get("name") == project.get("name")

    def test_get_all_project(self, client: TestClient):
        "Testa o retorno dos project"
        response = client.get("/project").json()
        assert isinstance(response, list)

    def test_get_specific_project(self, client: TestClient, project: ProjectDB):
        "Testa o retorno de um project"
        response = client.get(f"/project/?project_id={project.id}").json()
        print(response)
        print(project_database)
        assert response.get("name") == project.name
