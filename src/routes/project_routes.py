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
        if project_id not in project_database:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"project of id {project_id} not found"
                )
        return project_database[project_id]
    return list(project_database.values())

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjectDB)
def post_project(q: ProjectSchema):
    "Salvar project"
    if len(project_database) == 0:
        new_id = 1
    else:
        new_id = max(project_database)+1
    register = ProjectDB(
        id=new_id, created_at=datetime.now(),
        updated_at=datetime.now(), **q.model_dump()
        )
    project_database[new_id] = register
    return register

@router.put("/{project_id}", status_code=HTTPStatus.OK, response_model=ProjectDB)
def put_project(project_id: int, q: ProjectSchema):
    "Modificar project"
    if project_id not in project_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    project = project_database[project_id].model_dump()
    registry = ProjectDB(
        id=project_id, created_at=project['created_at'],
        updated_at=datetime.now(), **q.model_dump()
        )
    project_database[project_id] = registry
    return registry

@router.delete("/{project_id}", status_code=HTTPStatus.OK)
def delete_project(project_id: int):
    "Excluir project"
    if project_id not in project_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    project = project_database[project_id]
    del project_database[project_id]
    return project
