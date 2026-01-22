from pydantic import BaseModel, Field


class TagRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True