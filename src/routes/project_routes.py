"Rotas para project"

from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from db.database import project_database
from src.schemas.project_schema import ProjectSchema, ProjectDB

router = APIRouter(prefix="/project", tags=['Project'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ProjectDB] | ProjectDB)
def get_project(project_id: int | None = None):
    "Buscar project ou lista de project"
    if project_id:
        if len(project_database) < project_id or project_id < 1:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"project of id {project_id} not found"
                )

        found_project = project_database[project_id - 1]
        return found_project

    return project_database

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjectDB)
def post_project(q: ProjectSchema):
    "Salvar project"
    register = ProjectDB(
        id=len(project_database)+1, created_at=datetime.now(),
        updated_at=datetime.now(), **q.model_dump()
        )
    project_database.append(register)
    return register

@router.put("/{id}", status_code=HTTPStatus.OK, response_model=ProjectDB)
def put_project(project_id: int, q: ProjectSchema):
    "Modificar project"
    if project_id > len(project_database) or project_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")

    project = project_database[project_id - 1].model_dump()
    registry = ProjectDB(
        id=project_id, created_at=project['created_at'],
        updated_at=datetime.now(), **q.model_dump()
        )

    project_database[project_id - 1] = registry
    return registry

@router.delete("/", status_code=HTTPStatus.OK)
def delete_project(project_id: int):
    "Excluir project"
    if len(project_database) < project_id or project_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")

    project = project_database.pop(project_id - 1)
    return project
