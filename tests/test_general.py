"Testa a busca de todos os parâmetros"

from fastapi.testclient import TestClient

class TestAll:
    "Classe para testar o retorno dos bancos"
    def get_all(self, client: TestClient):
        "Verifica o retorno da busca geral"
        response = client.get("/getall").json()
        assert isinstance(response.get("Project"), list)
        assert isinstance(response.get("Client"), list)
        assert isinstance(response.get("Activity"), list)
