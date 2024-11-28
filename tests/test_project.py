"Testes para project"

from http import HTTPStatus
from fastapi.testclient import TestClient
from src.schemas.project_schema import ProjectDB

class TestProject:
    "Objeto de testes para project"
    def test_create_project(self, client: TestClient):
        "Testa a criação de um project"
        project = {
            "name": "testProject",
            "status": "testStatus"
        }
        response = client.post("/project", json=project).json()
        assert response.get("name") == project.get("name")
        assert response.get("status") == project.get("status")

    def test_get_all_project(self, client: TestClient):
        "Testa o retorno dos project"
        response = client.get("/project").json()
        assert isinstance(response, list)

    def test_get_specific_project(self, client: TestClient, project: ProjectDB):
        "Testa o retorno de um project"
        response = client.get("/project/", params={"project_id": project.id}).json()
        assert response.get("name") == project.name
        assert response.get("status") == project.status

    def test_get_specific_project_not_found(self, client: TestClient):
        "Testa o retorno de um project que não existe"
        response = client.get("/project/", params={"project_id": -1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_put_project(self, client: TestClient, project: ProjectDB):
        "Testa a atualização de um project"
        new_data = {
            "name": "NEW",
            "status": "NEW"
        }
        response = client.put(f"/project/{project.id}", json=new_data).json()
        assert response.get("name") == new_data['name']
        assert response.get("status") == new_data['status']

    def test_put_project_not_found(self, client: TestClient):
        "Testa a atualização de um project que não existe"
        new_data = {
            "name": "NEW",
            "status": "NEW"
        }
        response = client.put(f"/project/{-1}", json=new_data)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_project(self, client: TestClient, project: ProjectDB):
        "Testa a exclusão de um project"
        response = client.delete(f"/project/{project.id}")
        assert response.status_code == HTTPStatus.OK

    def test_delete_project_not_found(self, client: TestClient):
        "Testa a exclusão de um project que não existe"
        response = client.delete(f"/project/{-1}")
        assert response.status_code == HTTPStatus.NOT_FOUND
