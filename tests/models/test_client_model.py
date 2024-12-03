"Testes para ClientModel"

from sqlalchemy.orm import Session
from src.models.client_model import ClientModel


class TestClientModel:
    "Classe para testes de ClientModel"

    def test_create_client_model(self, session: Session):
        "Testa se o objeto do model é criado corretamente"
        client_name = "testClientModel"
        client_model = ClientModel(name=client_name, project_id=1)

        session.add(client_model)
        session.commit()
        session.refresh(client_model)

        assert client_model.name == client_name
        assert client_model.project_id
        assert client_model.id
        assert client_model.created_at
