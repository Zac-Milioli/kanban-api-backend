"Rotas para activity"

from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, join
from src.schemas.activity_schema import ActivitySchema, ActivityDB
from src.models.activity_model import ActivityModel
from src.models.client_model import ClientModel
from src.models.project_model import ProjectModel
from src.utils.database import get_session

router = APIRouter(prefix="/activity", tags=['Activity'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ActivityDB] | ActivityDB)
def get_activity(activity_id: int | None = None, client_id: int | None = None,
                    project_id: int | None = None, session: Session = Depends(get_session)):
    "Buscar activity ou lista de activity"
    if activity_id:
        activity_db = session.scalar(select(ActivityModel).where(ActivityModel.id == activity_id))
        if not activity_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="activity not found")
        return activity_db

    if client_id:
        client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
        if not client_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")
        activity_db = session.scalars(select(ActivityModel).where(ActivityModel.client_id == client_id))
        return activity_db

    if project_id:
        project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
        if not project_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="project not found")
        mask = select(ActivityModel).join(ClientModel, ActivityModel.client_id == ClientModel.id).where(ClientModel.project_id == project_id)
        activity_db = session.scalars(mask).all()
        return activity_db

    activity_db = session.scalars(select(ActivityModel))
    return activity_db

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ActivityDB)
def post_activity(q: ActivitySchema, session: Session = Depends(get_session)):
    "Salvar activity"
    client_id = q.model_dump()['client_id']
    client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
    if not client_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")

    activity_db = session.scalar(select(ActivityModel).where(ActivityModel.name == q.name))
    if activity_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="activity already exists")

    activity_db = ActivityModel(**q.model_dump())

    session.add(activity_db)
    session.commit()
    session.refresh(activity_db)

    return activity_db

@router.put("/{activity_id}", status_code=HTTPStatus.OK, response_model=ActivityDB)
def put_activity(activity_id: int, q: ActivitySchema, session: Session = Depends(get_session)):
    "Modificar activity"
    client_id = q.model_dump()['client_id']
    client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
    if not client_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")

    activity_db = session.scalar(select(ActivityModel).where(ActivityModel.id == activity_id))
    if not activity_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="activity not found")

    if activity_db.name != q.name:
        activity_same_name = session.scalar(select(ActivityModel).where(ActivityModel.name == q.name))
        if activity_same_name:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="activity already exists")
        activity_db.name = q.name
    
    activity_db.description = q.description
    activity_db.client_id = q.client_id
    activity_db.status = q.status

    session.commit()
    session.refresh(activity_db)

    return activity_db

@router.delete("/{activity_id}", status_code=HTTPStatus.OK)
def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    "Excluir activity"
    activity_db = session.scalar(select(ActivityModel).where(ActivityModel.id == activity_id))
    if not activity_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="id not found")
    session.delete(activity_db)
    session.commit()
    return activity_db
