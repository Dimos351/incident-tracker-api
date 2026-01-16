from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from typing import List, Optional
from enum import Enum


class IncidentStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class IncidentPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


# -------------------------------
# Base schema (for Create)
# -------------------------------
class IncidentBase(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=200,
        description="Short incident title."
    )

    description = Optional[str] = Field(
        None,
        max_length=5000,
    )

    priority = IncidentPriority = Field(
        IncidentPriority.medium,
        description="Incident priority"
    )

# -------------------------------
# Create schema
# -------------------------------
class IncidentCreate(IncidentBase):
    project_id: int = Field(
        ...,
        gt=0,
        description="Project ID inside organixation",
    )

    tags: List[str] = Field(
        default_factory=list,
        description="List of tag name"
    ) 

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        if len(v) > 10:
            raise ValueError("Cannot have more than 10 tags")
        clean_tags = []
        for tag in v:
            tag = tag.strip().lower()
            if tag:
                clean_tags.append(tag)
        return list(dict.fromkeys(clean_tags))
    
# -------------------------------
# Update schema (PATCH-like)
# -------------------------------
class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=200,
    )

    description: Optional[str] = Field(
        None,
        max_length=5000,
    )

    status: Optional[IncidentStatus] = None

    priority: Optional[IncidentPriority] = None

    assignee_to_id: Optional[int] = Field(
        None,
        gt=0
    )

    tags: Optional[List[str]] = Field(
        None,
        description="Optional list of tag name"
    )

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        if len(v) > 10:
            raise ValueError("Cannot have more than 10 tags")
        clean_tags = []
        for tag in v:
            tag = tag.strip().lower()
            if tag:
                clean_tags.append(tag)
        return list(dict.fromkeys(clean_tags))

# -------------------------------
# Read schema
# -------------------------------
class IncidentRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: IncidentStatus
    priority: IncidentPriority
    created_by_id: int | None
    assigned_to_id: int | None
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True