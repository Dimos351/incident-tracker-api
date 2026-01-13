from pydantic import BaseModel
from datetime import datetime

class IncidentCreate(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    priority: str = "medium"

class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_to_id: int | None = None

class IncidentRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_by_id: int | None
    assigned_to_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
