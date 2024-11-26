"Rotas para activity"

from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from db.database import activity_database, client_database
from src.schemas.activity_schema import ActivitySchema, ActivityDB

router = APIRouter(prefix="/activity", tags=['Activity'])

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ActivityDB] | ActivityDB)
def get_activity(activity_id: int | None = None):
    "Buscar activity ou lista de activity"
    if activity_id:
        if len(activity_database) < activity_id or activity_id < 1:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"Activity of id {activity_id} not found"
                )

        found_activity = activity_database[activity_id - 1]
        return found_activity

    return activity_database

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ActivityDB)
def post_activity(q: ActivitySchema):
    "Salvar activity"
    client_id = q.model_dump()['client_id']
    if client_id > len(client_database) or client_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="client not found")

    register = ActivityDB(
        id=len(activity_database)+1, created_at=datetime.now(),
        updated_at=datetime.now(), **q.model_dump()
        )
    activity_database.append(register)
    return register

@router.put("/{id}", status_code=HTTPStatus.OK, response_model=ActivityDB)
def put_activity(activity_id: int, q: ActivitySchema):
    "Modificar activity"
    client_id = q.model_dump()['client_id']
    if client_id > len(client_database) or client_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="client not found")
    if len(activity_database) < activity_id or activity_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")

    activity = activity_database[activity_id - 1].model_dump()
    registry = ActivityDB(
        id=activity_id, created_at=activity['created_at'],
        updated_at=datetime.now(), **q.model_dump()
        )

    activity_database[activity_id - 1] = registry
    return registry

@router.delete("/", status_code=HTTPStatus.OK)
def delete_activity(activity_id: int):
    "Excluir activity"
    if len(activity_database) < activity_id or activity_id < 1:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="id not found")

    activity = activity_database.pop(activity_id - 1)
    return activity
