"""In-memory storage for PromptLab.

This module provides simple in-memory storage for prompts, collections,
and their version histories. In a production environment, this would be
replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, PromptVersion, CollectionVersion, get_current_time


class Storage:
    """In-memory storage for prompts, collections, and their versions.

    This class simulates a database using Python dictionaries to store
    prompts, collections, and version snapshots. It provides methods to
    perform CRUD operations and version tracking on these entities.
    """

    def __init__(self):
        """Initialize the Storage with empty dictionaries for all entities."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._prompt_versions: Dict[str, List[PromptVersion]] = {}
        self._collection_versions: Dict[str, List[CollectionVersion]] = {}

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt and create its initial version snapshot.

        Args:
            prompt (Prompt): The prompt object to store.

        Returns:
            Prompt: The stored prompt object.
        """
        self._prompts[prompt.id] = prompt
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
        """Retrieve a prompt by its unique ID.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Optional[Prompt]: The prompt object if found, otherwise None.
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts currently stored.

        Returns:
            List[Prompt]: A list of all prompts in storage.
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt and create a new version snapshot.

        Increments the version number and stores a snapshot of the updated
        prompt data in the version history.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The updated prompt object.

        Returns:
            Optional[Prompt]: The updated prompt if it exists, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        versions = self._prompt_versions.get(prompt_id, [])
        new_version_num = len(versions) + 1
        prompt.current_version = new_version_num
        self._prompts[prompt_id] = prompt
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
        """Delete a prompt and its version history by ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._prompt_versions.pop(prompt_id, None)
            return True
        return False

    def get_prompt_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Retrieve all version snapshots for a prompt.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            List[PromptVersion]: A list of all version snapshots, or empty list.
        """
        return self._prompt_versions.get(prompt_id, [])

    def get_prompt_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Retrieve a specific version snapshot of a prompt.

        Args:
            prompt_id (str): The unique identifier of the prompt.
            version (int): The version number to retrieve.

        Returns:
            Optional[PromptVersion]: The version snapshot if found, otherwise None.
        """
        versions = self._prompt_versions.get(prompt_id, [])
        for v in versions:
            if v.version == version:
                return v
        return None

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection and create its initial version snapshot.

        Args:
            collection (Collection): The collection object to store.

        Returns:
            Collection: The stored collection object.
        """
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
        """Retrieve a collection by its unique ID.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            Optional[Collection]: The collection object if found, otherwise None.
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections currently stored.

        Returns:
            List[Collection]: A list of all collections in storage.
        """
        return list(self._collections.values())

    def update_collection(self, collection_id: str, collection: Collection) -> Optional[Collection]:
        """Update an existing collection and create a new version snapshot.

        Increments the version number and stores a snapshot of the updated
        collection data in the version history.

        Args:
            collection_id (str): The unique identifier of the collection to update.
            collection (Collection): The updated collection object.

        Returns:
            Optional[Collection]: The updated collection if it exists, otherwise None.
        """
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
        """Delete a collection and its version history by ID.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            self._collection_versions.pop(collection_id, None)
            return True
        return False

    def get_collection_versions(self, collection_id: str) -> List[CollectionVersion]:
        """Retrieve all version snapshots for a collection.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[CollectionVersion]: A list of all version snapshots, or empty list.
        """
        return self._collection_versions.get(collection_id, [])

    def get_collection_version(self, collection_id: str, version: int) -> Optional[CollectionVersion]:
        """Retrieve a specific version snapshot of a collection.

        Args:
            collection_id (str): The unique identifier of the collection.
            version (int): The version number to retrieve.

        Returns:
            Optional[CollectionVersion]: The version snapshot if found, otherwise None.
        """
        versions = self._collection_versions.get(collection_id, [])
        for v in versions:
            if v.version == version:
                return v
        return None

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[Prompt]: A list of prompts belonging to the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def clear(self):
        """Clear all stored prompts, collections, and their version histories."""
        self._prompts.clear()
        self._collections.clear()
        self._prompt_versions.clear()
        self._collection_versions.clear()


storage = Storage()
