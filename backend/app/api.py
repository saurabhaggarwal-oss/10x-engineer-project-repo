"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate, CollectionUpdate,
    PromptList, CollectionList,
    PromptVersionList, CollectionVersionList,
    PromptVersion, CollectionVersion,
    HealthResponse, get_current_time,
)
from app.storage import storage
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    filter_prompts_by_tags,
)
from app import __version__

app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__,
)

# Seed initial data
from app.seed import seed_data
seed_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Helpers ==============


def _get_prompt_or_404(prompt_id: str) -> Prompt:
    prompt = storage.get_prompt(prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def _get_collection_or_404(collection_id: str) -> Collection:
    collection = storage.get_collection(collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


def _validate_collection_exists(collection_id: Optional[str]) -> None:
    if collection_id and not storage.get_collection(collection_id):
        raise HTTPException(status_code=400, detail="Collection not found")


# ============== Health Check ==============


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============


@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None,
) -> PromptList:
    prompts = storage.get_all_prompts()
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        prompts = filter_prompts_by_tags(prompts, tag_list)
    if search:
        prompts = search_prompts(prompts, search)
    prompts = sort_prompts_by_date(prompts, descending=True)
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    return _get_prompt_or_404(prompt_id)


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    _validate_collection_exists(prompt_data.collection_id)
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    existing = _get_prompt_or_404(prompt_id)
    _validate_collection_exists(prompt_data.collection_id)
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=prompt_data.tags,
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: Dict[str, Any]) -> Prompt:
    existing = _get_prompt_or_404(prompt_id)
    for key, value in prompt_data.items():
        if hasattr(existing, key) and value is not None:
            setattr(existing, key, value)
    existing.updated_at = get_current_time()
    return storage.update_prompt(prompt_id, existing)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")


@app.put("/prompts/{prompt_id}/tags", response_model=Prompt)
def set_prompt_tags(prompt_id: str, tags: List[str]) -> Prompt:
    existing = _get_prompt_or_404(prompt_id)
    existing.tags = tags
    existing.updated_at = get_current_time()
    return storage.update_prompt(prompt_id, existing)


# ============== Prompt Version Endpoints ==============


@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def list_prompt_versions(prompt_id: str) -> PromptVersionList:
    _get_prompt_or_404(prompt_id)
    versions = storage.get_prompt_versions(prompt_id)
    return PromptVersionList(versions=versions, total=len(versions))


@app.get("/prompts/{prompt_id}/versions/{version}", response_model=PromptVersion)
def get_prompt_version(prompt_id: str, version: int) -> PromptVersion:
    _get_prompt_or_404(prompt_id)
    v = storage.get_prompt_version(prompt_id, version)
    if v is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return v


# ============== Collection Endpoints ==============


@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    return _get_collection_or_404(collection_id)


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.put("/collections/{collection_id}", response_model=Collection)
def update_collection(collection_id: str, collection_data: CollectionUpdate) -> Collection:
    existing = _get_collection_or_404(collection_id)
    existing.name = collection_data.name
    existing.description = collection_data.description
    return storage.update_collection(collection_id, existing)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    for prompt in storage.get_prompts_by_collection(collection_id):
        prompt.collection_id = None
        storage.update_prompt(prompt.id, prompt)


# ============== Collection Version Endpoints ==============


@app.get("/collections/{collection_id}/versions", response_model=CollectionVersionList)
def list_collection_versions(collection_id: str) -> CollectionVersionList:
    _get_collection_or_404(collection_id)
    versions = storage.get_collection_versions(collection_id)
    return CollectionVersionList(versions=versions, total=len(versions))


@app.get("/collections/{collection_id}/versions/{version}", response_model=CollectionVersion)
def get_collection_version(collection_id: str, version: int) -> CollectionVersion:
    _get_collection_or_404(collection_id)
    v = storage.get_collection_version(collection_id, version)
    if v is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return v
