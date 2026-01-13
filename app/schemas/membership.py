from pydantic import BaseModel

class MembershipRead(BaseModel):
    user_id: int
    role: str

    class Config:
        from_attributes = True