"Testes para client"

from http import HTTPStatus
from fastapi.testclient import TestClient
from src.schemas.client_schema import ClientDB
from src.schemas.project_schema import ProjectDB

class TestClientInstance:
    "Objeto de testes para client"
    def test_create_client(self, client: TestClient, project: ProjectDB):
        "Testa a criação de um client"
        test_client = {
            "name": "testclient",
            "project_id": project.id
        }
        response = client.post("/client", json=test_client)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json().get("name") == test_client.get("name")
        assert response.json().get("project_id") == project.id

    def test_get_all_client(self, client: TestClient):
        "Testa o retorno dos client"
        response = client.get("/client").json()
        assert isinstance(response, list)

    def test_get_specific_client(self, client: TestClient, client_instance: ClientDB):
        "Testa o retorno de um client"
        response = client.get("/client/", params={"client_id": client_instance.id}).json()
        assert response.get("name") == client_instance.name

    def test_get_client_from_project(self, client: TestClient, client_instance: ClientDB):
        "Testa o retorno dos client de um project"
        response = client.get("/client/", params={"project_id": client_instance.project_id})
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), list)
        assert ClientDB(**response.json()[0]) == client_instance

    def test_get_specific_client_not_found(self, client: TestClient):
        "Testa o retorno de um client que não existe"
        response = client.get("/client/", params={"client_id": -1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_put_client(self, client: TestClient, client_instance: ClientDB):
        "Testa a atualização de um client"
        new_data = {
            "name": "NEW",
            "project_id": client_instance.project_id
        }
        response = client.put(f"/client/{client_instance.id}", json=new_data).json()
        assert response.get("name") == new_data['name']
        assert response.get("project_id") == client_instance.project_id

    def test_put_client_not_found(self, client: TestClient):
        "Testa a atualização de um client que não existe"
        new_data = {
            "name": "NEW",
            "project_id": 1
        }
        response = client.put(f"/client/{-1}", json=new_data)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_client(self, client: TestClient, client_instance: ClientDB):
        "Testa a exclusão de um client"
        response = client.delete(f"/client/{client_instance.id}")
        assert response.status_code == HTTPStatus.OK

    def test_delete_client_not_found(self, client: TestClient):
        "Testa a exclusão de um client que não existe"
        response = client.delete(f"/client/{-1}")
        assert response.status_code == HTTPStatus.NOT_FOUND
