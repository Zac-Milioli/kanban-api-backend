"Arquivo principal do sistema"

from fastapi import FastAPI
import uvicorn
from src.routes.activity_routes import router as activity_router

app = FastAPI()
app.include_router(activity_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
