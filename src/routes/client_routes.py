"Rotas para client"

from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from src.schemas.client_schema import ClientDB, ClientSchema
from db.database import client_database, project_database

router = APIRouter(prefix="/client", tags=['Client'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ClientDB] | ClientDB)
def get_client(client_id: int | None = None):
    "Buscar client ou lista de client"
    if client_id:
        if len(client_database) < client_id or client_id < 1:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"client of id {client_id} not found"
                )

        found_client = client_database[client_id - 1]
        return found_client

    return client_database

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientDB)
def post_client(q: ClientSchema):
    "Salvar client"
    project_id = q.model_dump()['project_id']
    if project_id > len(project_database) or project_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    register = ClientDB(
        id=len(client_database)+1, created_at=datetime.now(),
        updated_at=datetime.now(), **q.model_dump()
        )
    client_database.append(register)
    return register

@router.put("/{client_id}", status_code=HTTPStatus.OK, response_model=ClientDB)
def put_client(client_id: int, q: ClientSchema):
    "Modificar client"
    project_id = q.model_dump()['project_id']
    if project_id > len(project_database) or project_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="project not found")
    if len(client_database) < client_id or client_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")

    client = client_database[client_id - 1].model_dump()
    registry = ClientDB(
        id=client_id, created_at=client['created_at'],
        updated_at=datetime.now(), **q.model_dump()
        )

    client_database[client_id - 1] = registry
    return registry

@router.delete("/{client_id}", status_code=HTTPStatus.OK)
def delete_client(client_id: int):
    "Excluir client"
    if len(client_database) < client_id or client_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")

    client = client_database.pop(client_id - 1)
    return client
