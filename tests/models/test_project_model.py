"Testes para ProjectModel"

from datetime import datetime
from sqlalchemy import create_engine
from src.models.project_model import ProjectModel, table_registry

class TestProjectModel:
    "Classe para testes de ProjectModel"
    def test_create_project_model(self):
        "Testa se o objeto do model é criado corretamente"
        engine = create_engine('sqlite:///:memory:')
        table_registry.metadata.create_all(engine)

        project_name = "testProjectModel"
        project_model = ProjectModel(name=project_name, status="testStatus")
        assert project_model.name == project_name
