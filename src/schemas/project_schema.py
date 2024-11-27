"Schemas para project"

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProjectSchema(BaseModel):
    "Formato de entrada de project"
    name: str
    status: str
    model_config = ConfigDict(from_attributes=True)

class ProjectDB(ProjectSchema):
    "Formato de registro de project"
    id: int
    created_at: datetime
    updated_at: datetime
