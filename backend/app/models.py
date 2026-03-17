"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def generate_id() -> str:
    """Generate a unique identifier using UUID4."""
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time."""
    return datetime.utcnow()


# ============== Version Models ==============


class PromptVersion(BaseModel):
    """Snapshot of a prompt at a point in time."""
    version: int = Field(description="Version number.")
    title: str = Field(description="Title at this version.")
    content: str = Field(description="Content at this version.")
    description: Optional[str] = Field(None, description="Description at this version.")
    collection_id: Optional[str] = Field(None, description="Collection ID at this version.")
    tags: List[str] = Field(default_factory=list, description="Tags at this version.")
    created_at: datetime = Field(default_factory=get_current_time, description="When this version was created.")


class CollectionVersion(BaseModel):
    """Snapshot of a collection at a point in time."""
    version: int = Field(description="Version number.")
    name: str = Field(description="Name at this version.")
    description: Optional[str] = Field(None, description="Description at this version.")
    created_at: datetime = Field(default_factory=get_current_time, description="When this version was created.")


# ============== Prompt Models ==============


class PromptBase(BaseModel):
    """Base model for prompts containing common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the prompt.")
    content: str = Field(..., min_length=1, description="Content or body of the prompt.")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the prompt.")
    collection_id: Optional[str] = Field(None, description="Identifier of the collection to which the prompt belongs.")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the prompt.")


class PromptCreate(PromptBase):
    """Model for creating a new prompt."""
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt."""
    pass


class Prompt(PromptBase):
    """Model representing a prompt including its metadata."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_id, description="Unique identifier for the prompt.")
    current_version: int = Field(default=1, description="Current version number.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was created.")
    updated_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was last updated.")


# ============== Collection Models ==============


class CollectionBase(BaseModel):
    """Base model for collections containing common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the collection.")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the collection.")


class CollectionCreate(CollectionBase):
    """Model for creating a new collection."""
    pass


class CollectionUpdate(CollectionBase):
    """Model for updating a collection."""
    pass


class Collection(CollectionBase):
    """Model representing a collection including its metadata."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_id, description="Unique identifier for the collection.")
    current_version: int = Field(default=1, description="Current version number.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the collection was created.")


# ============== Response Models ==============


class PromptList(BaseModel):
    """Response model for a list of prompts."""
    prompts: List[Prompt] = Field(description="List of prompt objects.")
    total: int = Field(description="Total number of prompts available.")


class CollectionList(BaseModel):
    """Response model for a list of collections."""
    collections: List[Collection] = Field(description="List of collection objects.")
    total: int = Field(description="Total number of collections available.")


class PromptVersionList(BaseModel):
    """Response model for prompt version history."""
    versions: List[PromptVersion] = Field(description="List of prompt versions.")
    total: int = Field(description="Total number of versions.")


class CollectionVersionList(BaseModel):
    """Response model for collection version history."""
    versions: List[CollectionVersion] = Field(description="List of collection versions.")
    total: int = Field(description="Total number of versions.")


class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(description="Current status of the application.")
    version: str = Field(description="Current version of the application.")
