"""Cache management for markdown processing."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class CacheManager:
    """Manage caching of processed markdown files using MD5 hashes."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory to store cache files. Defaults to .babbl_cache
        """
        self.cache_dir = cache_dir or Path(".babbl_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "cache.json"
        self.cache_data: dict[str, Any] = self._load_cache()

    def _load_cache(self) -> dict[str, Any]:
        """Load cache data from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self):
        """Save cache data to disk."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")

    def _calculate_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of a file.

        Args:
            file_path: Path to the file

        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError:
            return ""

    def _calculate_content_hash(self, content: str) -> str:
        """
        Calculate MD5 hash of content string.

        Args:
            content: Content to hash

        Returns:
            MD5 hash string
        """
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def get_cache_key(self, file_path: Path) -> str:
        """
        Generate cache key for a file.

        Args:
            file_path: Path to the file

        Returns:
            Cache key string
        """
        return str(file_path.absolute())

    def is_stale(self, file_path: Path) -> bool:
        """
        Check if a file needs to be regenerated.

        Args:
            file_path: Path to the file to check

        Returns:
            True if file needs regeneration, False if cache is valid
        """
        cache_key = self.get_cache_key(file_path)

        if cache_key not in self.cache_data:
            return True

        current_hash = self._calculate_hash(file_path)
        cached_hash = self.cache_data[cache_key].get("hash", "")

        return current_hash != cached_hash

    def is_content_stale(self, file_path: Path, content: str) -> bool:
        """
        Check if content needs to be regenerated.

        Args:
            file_path: Path to the file
            content: Current content

        Returns:
            True if content needs regeneration, False if cache is valid
        """
        cache_key = self.get_cache_key(file_path)

        if cache_key not in self.cache_data:
            return True

        current_hash = self._calculate_content_hash(content)
        cached_hash = self.cache_data[cache_key].get("content_hash", "")

        return current_hash != cached_hash

    def update_cache(
        self,
        file_path: Path,
        output_path: Path,
        content_hash: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Update cache for a processed file.

        Args:
            file_path: Path to the source file
            output_path: Path to the generated output file
            content_hash: Hash of the processed content (optional)
            metadata: Additional metadata to store (optional)
        """
        cache_key = self.get_cache_key(file_path)
        file_hash = self._calculate_hash(file_path)

        cache_entry = {
            "hash": file_hash,
            "output_path": str(output_path),
            "last_processed": datetime.now().isoformat(),
        }

        if content_hash:
            cache_entry["content_hash"] = content_hash

        if metadata:
            cache_entry["metadata"] = metadata

        self.cache_data[cache_key] = cache_entry
        self._save_cache()

    def get_cached_output_path(self, file_path: Path) -> Optional[Path]:
        """
        Get the cached output path for a file.

        Args:
            file_path: Path to the source file

        Returns:
            Path to cached output file or None if not cached
        """
        cache_key = self.get_cache_key(file_path)

        if cache_key in self.cache_data:
            output_path_str = self.cache_data[cache_key].get("output_path")
            if output_path_str:
                output_path = Path(output_path_str)
                if output_path.exists():
                    return output_path

        return None

    def clear_cache(self):
        """Clear all cached data."""
        self.cache_data = {}
        self._save_cache()

    def remove_from_cache(self, file_path: Path):
        """
        Remove a specific file from cache.

        Args:
            file_path: Path to the file to remove from cache
        """
        cache_key = self.get_cache_key(file_path)
        if cache_key in self.cache_data:
            del self.cache_data[cache_key]
            self._save_cache()
