"Testes para ProjectModel"

from sqlalchemy.orm import Session
from src.models.project_model import ProjectModel

class TestProjectModel:
    "Classe para testes de ProjectModel"
    def test_create_project_model(self, session: Session):
        "Testa se o objeto do model é criado corretamente"
        project_name = "testProjectModel"
        project_model = ProjectModel(name=project_name, status="testStatus")

        session.add(project_model)
        session.commit()
        session.refresh(project_model)
        
        assert project_model.name == project_name
        assert project_model.id
        assert project_model.created_at
