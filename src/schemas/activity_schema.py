"Schemas para activity"

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ActivitySchema(BaseModel):
    "Formato de entrada de activity"
    name: str
    description: str | None = None
    status: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ActivityDB(ActivitySchema):
    "Formato de registro de activity"
    id: int
    created_at: datetime
    updated_at: datetime