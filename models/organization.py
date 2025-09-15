# models/organization.py

from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class OrganizationBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Organization ID (server-generated).",
        json_schema_extra={"example": "c1ea8c44-9c82-40c4-9fa8-b2fd3f5f6214"},
    )
    name: str = Field(
        ...,
        description="Organization name.",
        json_schema_extra={"example": "Quantum AI Research Lab"},
    )
    description: Optional[str] = Field(
        None,
        description="Short description of the organization.",
        json_schema_extra={"example": "A lab focusing on quantum computing and AI integration."},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "c1ea8c44-9c82-40c4-9fa8-b2fd3f5f6214",
                    "name": "Quantum AI Research Lab",
                    "description": "A lab focusing on quantum computing and AI integration.",
                }
            ]
        }
    }

class OrganizationCreate(OrganizationBase):
    """Creation payload for an Organization."""
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Organization name.")
    description: Optional[str] = Field(None, description="Description.")

class OrganizationRead(OrganizationBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
    )
