"Rotas para client"

from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from src.schemas.client_schema import ClientDB, ClientSchema
from db.database import client_database, project_database

router = APIRouter(prefix="/client", tags=['Client'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ClientDB] | ClientDB)
def get_client(client_id: int | None = None, project_id: int | None = None):
    "Buscar client ou lista de client"
    if client_id:
        if client_id not in client_database:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"client of id {client_id} not found"
                )
        return client_database[client_id]
    if project_id:
        if project_id not in project_database:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"project of id {project_id} not found"
                )
        return [client for client in client_database.values() if client.project_id == project_id]
    return list(client_database.values())

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientDB)
def post_client(q: ClientSchema):
    "Salvar client"
    project_id = q.model_dump()['project_id']
    if project_id not in project_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    if len(client_database) == 0:
        new_id = 1
    else:
        new_id = max(client_database)+1
    register = ClientDB(
        id=new_id, created_at=datetime.now(),
        updated_at=datetime.now(), **q.model_dump()
        )
    client_database[new_id] = register
    return register

@router.put("/{client_id}", status_code=HTTPStatus.OK, response_model=ClientDB)
def put_client(client_id: int, q: ClientSchema):
    "Modificar client"
    project_id = q.model_dump()['project_id']
    if project_id not in project_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    if client_id not in client_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")

    client = client_database[client_id].model_dump()
    registry = ClientDB(
        id=client_id, created_at=client['created_at'],
        updated_at=datetime.now(), **q.model_dump()
        )
    client_database[client_id] = registry
    return registry

@router.delete("/{client_id}", status_code=HTTPStatus.OK)
def delete_client(client_id: int):
    "Excluir client"
    if client_id not in client_database:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")
    client = client_database[client_id]
    del client_database[client_id]
    return client
