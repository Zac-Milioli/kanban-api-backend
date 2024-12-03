"Schemas para client"

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClientSchema(BaseModel):
    "Formato de entrada de client"
    name: str
    project_id: int
    model_config = ConfigDict(from_attributes=True)


class ClientDB(ClientSchema):
    "Formato de registro de client"
    id: int
    created_at: datetime
    updated_at: datetime
