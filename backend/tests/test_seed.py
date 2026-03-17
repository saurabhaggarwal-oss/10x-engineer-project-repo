"""Tests for seed data module."""

from app.seed import seed_data
from app.storage import storage


class TestSeedData:
    """Tests for the seed_data function."""

    def test_seed_populates_data(self):
        seed_data()
        assert len(storage.get_all_collections()) == 5
        assert len(storage.get_all_prompts()) == 10

    def test_seed_does_not_run_twice(self):
        seed_data()
        # Capture counts after first seed
        collections_count = len(storage.get_all_collections())
        prompts_count = len(storage.get_all_prompts())
        # Run again — should early return
        seed_data()
        assert len(storage.get_all_collections()) == collections_count
        assert len(storage.get_all_prompts()) == prompts_count
