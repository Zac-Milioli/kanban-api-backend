"Arquivo principal do sistema"

from http import HTTPStatus
from fastapi import FastAPI
import uvicorn
from src.routes.activity_routes import router as activity_router
from src.routes.client_routes import router as client_router
from src.routes.project_routes import router as project_router
from db.database import client_database, activity_database, project_database

PART1 = "As **activity dependem** da existência de um **client** para serem criadas. "
PART2 = "Os **client dependem** de um **project**"

app = FastAPI(title="Kanban Backend",
            description=PART1+PART2)

@app.get("/getall", tags=["Get all data"], status_code=HTTPStatus.OK)
def get_all():
    "Retorna o banco completo"
    return {"Project": project_database, "Client": client_database, "Activity": activity_database}

app.include_router(project_router)
app.include_router(client_router)
app.include_router(activity_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
