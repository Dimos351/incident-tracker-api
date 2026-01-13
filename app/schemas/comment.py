from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    body: str = Field(
        ...,
        min_length=1,
        max_length=6_000,
        description="Comment text body",
    )

class CommentRead(BaseModel):
    id: int
    incident_id: int
    author_id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
