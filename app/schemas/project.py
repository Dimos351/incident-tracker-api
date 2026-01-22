from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255,
        examples=["Backend Platform"],
    )

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

class ProjectRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True