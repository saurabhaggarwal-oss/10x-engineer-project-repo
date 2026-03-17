"""In-memory storage for PromptLab"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, PromptVersion, CollectionVersion, get_current_time


class Storage:
    """In-memory storage for prompts, collections, and their versions."""

    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._prompt_versions: Dict[str, List[PromptVersion]] = {}
        self._collection_versions: Dict[str, List[CollectionVersion]] = {}

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        # Save initial version
        v = PromptVersion(
            version=1,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=prompt.collection_id,
            tags=prompt.tags,
            created_at=prompt.created_at,
        )
        self._prompt_versions[prompt.id] = [v]
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        # Bump version
        versions = self._prompt_versions.get(prompt_id, [])
        new_version_num = len(versions) + 1
        prompt.current_version = new_version_num
        self._prompts[prompt_id] = prompt
        # Save version snapshot
        v = PromptVersion(
            version=new_version_num,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=prompt.collection_id,
            tags=prompt.tags,
            created_at=get_current_time(),
        )
        versions.append(v)
        self._prompt_versions[prompt_id] = versions
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._prompt_versions.pop(prompt_id, None)
            return True
        return False

    def get_prompt_versions(self, prompt_id: str) -> List[PromptVersion]:
        return self._prompt_versions.get(prompt_id, [])

    def get_prompt_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        versions = self._prompt_versions.get(prompt_id, [])
        for v in versions:
            if v.version == version:
                return v
        return None

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        v = CollectionVersion(
            version=1,
            name=collection.name,
            description=collection.description,
            created_at=collection.created_at,
        )
        self._collection_versions[collection.id] = [v]
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())

    def update_collection(self, collection_id: str, collection: Collection) -> Optional[Collection]:
        if collection_id not in self._collections:
            return None
        versions = self._collection_versions.get(collection_id, [])
        new_version_num = len(versions) + 1
        collection.current_version = new_version_num
        self._collections[collection_id] = collection
        v = CollectionVersion(
            version=new_version_num,
            name=collection.name,
            description=collection.description,
            created_at=get_current_time(),
        )
        versions.append(v)
        self._collection_versions[collection_id] = versions
        return collection

    def delete_collection(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._collection_versions.pop(collection_id, None)
            return True
        return False

    def get_collection_versions(self, collection_id: str) -> List[CollectionVersion]:
        return self._collection_versions.get(collection_id, [])

    def get_collection_version(self, collection_id: str, version: int) -> Optional[CollectionVersion]:
        versions = self._collection_versions.get(collection_id, [])
        for v in versions:
            if v.version == version:
                return v
        return None

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def clear(self):
        self._prompts.clear()
        self._collections.clear()
        self._prompt_versions.clear()
        self._collection_versions.clear()


storage = Storage()
