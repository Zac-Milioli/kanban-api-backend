"Rotas para project"

from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.schemas.project_schema import ProjectSchema, ProjectDB
from src.utils.database import get_session
from src.models.project_model import ProjectModel

router = APIRouter(prefix="/project", tags=['Project'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ProjectDB] | ProjectDB)
def get_project(project_id: int | None = None, session: Session = Depends(get_session)):
    "Buscar project ou lista de project"
    if project_id:
        project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
        if not project_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="project not found")
        return project_db

    project_db = session.scalars(select(ProjectModel))
    return project_db

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjectDB)
def post_project(q: ProjectSchema, session: Session = Depends(get_session)):
    "Salvar project"
    project_db = session.scalar(select(ProjectModel).where(ProjectModel.name == q.name))
    if project_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="project already exists")

    project_db = ProjectModel(**q.model_dump())

    session.add(project_db)
    session.commit()
    session.refresh(project_db)

    return project_db

@router.put("/{project_id}", status_code=HTTPStatus.OK, response_model=ProjectDB)
def put_project(project_id: int, q: ProjectSchema, session: Session = Depends(get_session)):
    "Modificar project"
    project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
    if not project_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='project not found')

    if project_db.name != q.name:
        project_same_name = session.scalar(select(ProjectModel).where(ProjectModel.name == q.name))
        if project_same_name:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="project already exists")
        project_db.name = q.name

    project_db.status = q.status

    session.commit()
    session.refresh(project_db)

    return project_db


@router.delete("/{project_id}", status_code=HTTPStatus.OK)
def delete_project(project_id: int, session: Session = Depends(get_session)):
    "Excluir project"
    project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
    if not project_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='project not found')
    session.delete(project_db)
    session.commit()
    return project_db
