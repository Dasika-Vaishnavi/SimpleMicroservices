# models/project.py

from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Project ID (server-generated).",
        json_schema_extra={"example": "ffdfd2a2-9403-11ea-bb37-0242ac130002"},
    )
    title: str = Field(
        ...,
        description="Project title.",
        json_schema_extra={"example": "Explainable AI on Quantum Systems"},
    )
    summary: Optional[str] = Field(
        None,
        description="Short summary of the project.",
        json_schema_extra={"example": "Building interpretable models for hybrid quantum-classical systems."},
    )
    organization_id: Optional[UUID] = Field(
        None,
        description="Linked organization ID.",
        json_schema_extra={"example": "c1ea8c44-9c82-40c4-9fa8-b2fd3f5f6214"},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "ffdfd2a2-9403-11ea-bb37-0242ac130002",
                    "title": "Explainable AI on Quantum Systems",
                    "summary": "Building interpretable models for hybrid quantum-classical systems.",
                    "organization_id": "c1ea8c44-9c82-40c4-9fa8-b2fd3f5f6214",
                }
            ]
        }
    }

class ProjectCreate(ProjectBase):
    """Creation payload for a Project."""
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Project title.")
    summary: Optional[str] = Field(None, description="Summary.")
    organization_id: Optional[UUID] = Field(None, description="Linked organization ID.")

class ProjectRead(ProjectBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
    )
