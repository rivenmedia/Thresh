import json
from pathlib import Path
from typing import Optional

from utils import data_dir_path

from .models import AppModel


class SettingsManager:
    """Class that handles settings, ensuring they are validated against a Pydantic schema."""

    def __init__(self, filename: str = "settings.json"):
        self.filename = filename
        self.settings_file = data_dir_path / self.filename
        self.settings = self.load() if self.settings_file.exists() else self.create_default_settings()

    def create_default_settings(self) -> AppModel:
        """Create default settings and save them to file."""
        settings = AppModel()
        self.save(settings)
        return settings

    def load(self, settings_dict: Optional[dict] = None) -> AppModel:
        """Load settings from file, validating against the AppModel schema."""
        if settings_dict:
            return AppModel(**settings_dict)
        with open(self.settings_file, "r", encoding="utf-8") as file:
            settings_data = json.load(file)
            return AppModel(**settings_data)

    def save(self, settings: Optional[AppModel] = None):
        """Save settings to file, using Pydantic model for JSON serialization."""
        settings = settings or self.settings
        with open(self.settings_file, "w", encoding="utf-8") as file:
            file.write(settings.model_dump_json(indent=4))


settings_manager = SettingsManager()