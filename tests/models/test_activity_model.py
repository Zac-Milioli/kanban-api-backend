"Testes para ClientModel"

from sqlalchemy.orm import Session
from src.models.activity_model import ActivityModel

class TestActivityModel:
    "Classe para testes de ActivityModel"
    def test_create_client_model(self, session: Session):
        "Testa se o objeto do model é criado corretamente"
        activity_name = "testActivityModel"
        activity_description = None
        activity_model = ActivityModel(name=activity_name, client_id=1,
                                        description=activity_description,
                                        status="testStatus")

        session.add(activity_model)
        session.commit()
        session.refresh(activity_model)

        assert activity_model.name == activity_name
        assert activity_model.client_id
        assert activity_model.id
        assert activity_model.created_at
