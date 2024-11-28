"Testa a busca de todos os parâmetros"

from http import HTTPStatus
from fastapi.testclient import TestClient
from src.schemas.activity_schema import ActivityDB
from src.schemas.client_schema import ClientDB
from src.schemas.project_schema import ProjectDB
from db.database import project_database, client_database

class TestDatabase:
    "Classe para testar o retorno dos bancos"
    def test_get_database(self, client: TestClient, activity: ActivityDB):
        "Verifica o retorno da busca geral"
        response = client.get("/getall")
        assert response.status_code == HTTPStatus.OK
        response = response.json()
        assert isinstance(response.get("Project"), list)
        assert isinstance(response.get("Client"), list)
        assert isinstance(response.get("Activity"), list)
        assert ProjectDB(**response.get("Project")[0]) == project_database[1]
        assert ClientDB(**response.get("Client")[0]) == client_database[1]
        assert ActivityDB(**response.get("Activity")[0]) == activity
