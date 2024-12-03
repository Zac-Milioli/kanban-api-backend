"Rotas para client"

from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas.client_schema import ClientDB, ClientSchema
from src.models.client_model import ClientModel
from src.models.project_model import ProjectModel
from src.utils.database import get_session

router = APIRouter(prefix="/client", tags=['Client'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ClientDB] | ClientDB)
def get_client(client_id: int | None = None, project_id: int | None = None,
                session: Session = Depends(get_session)):
    "Buscar client ou lista de client"
    if client_id:
        client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
        if not client_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")
        return client_db

    if project_id:
        project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
        if not project_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="project not found")
        project_clients_db = session.scalars(
            select(ClientModel).where(ClientModel.project_id == project_id)
            )
        return project_clients_db

    clients_db = session.scalars(select(ClientModel))
    return clients_db

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientDB)
def post_client(q: ClientSchema, session: Session = Depends(get_session)):
    "Salvar client"
    project_id = q.model_dump()['project_id']

    project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
    if not project_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="project not found")

    client_db = session.scalar(select(ClientModel).where(ClientModel.name == q.name))
    if client_db:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="client already exists")

    client_db = ClientModel(**q.model_dump())

    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return client_db

@router.put("/{client_id}", status_code=HTTPStatus.OK, response_model=ClientDB)
def put_client(client_id: int, q: ClientSchema, session: Session = Depends(get_session)):
    "Modificar client"
    project_id = q.model_dump()['project_id']

    project_db = session.scalar(select(ProjectModel).where(ProjectModel.id == project_id))
    if not project_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="project not found")

    client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
    if not client_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")

    if client_db.name != q.name:
        client_same_name = session.scalar(select(ClientModel).where(ClientModel.name == q.name))
        if client_same_name:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="client already exists")
        client_db.name = q.name

    client_db.project_id = q.project_id

    session.commit()
    session.refresh(client_db)

    return client_db

@router.delete("/{client_id}", status_code=HTTPStatus.OK)
def delete_client(client_id: int, session: Session = Depends(get_session)):
    "Excluir client"
    client_db = session.scalar(select(ClientModel).where(ClientModel.id == client_id))
    if not client_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="client not found")
    session.delete(client_db)
    session.commit()
    return client_db
