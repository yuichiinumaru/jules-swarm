import os
from pathlib import Path
from typing import List, Optional

class SwarmConfig:
    def __init__(self, env_path: str = ".env"):
        self.env_path = Path(env_path)
        self.api_keys: List[str] = []
        self._load_env()
        self._load_keys()

    def _load_env(self):
        """Loads environment variables from .env file."""
        if not self.env_path.exists():
            # Try looking in parent directories or standard locations
            possible_paths = [
                Path("scripts/research/jules-swarm/.env"),
                Path(".env"),
                Path("../.env")
            ]
            for p in possible_paths:
                if p.exists():
                    self.env_path = p
                    break
        
        if self.env_path.exists():
            with open(self.env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

    def _load_keys(self):
        """Loads API keys from environment."""
        # Try plural first
        val = os.environ.get("JULES_API_KEYS")
        if val:
            self.api_keys = [k.strip() for k in val.split(",") if k.strip()]
            return

        # Fallback to singular
        single_val = os.environ.get("JULES_API_KEY")
        if single_val:
            self.api_keys = [single_val]

    def get_api_key(self, index: int = 0) -> str:
        """Returns API key with round-robin support."""
        if not self.api_keys:
            raise ValueError("No JULES_API_KEYS found in environment or .env file.")
        return self.api_keys[index % len(self.api_keys)]

    @property
    def api_base_url(self) -> str:
        return os.environ.get("JULES_API_BASE", "https://jules.googleapis.com/v1alpha")
