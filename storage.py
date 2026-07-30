import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from config import SEEN_JOBS_FILE, BASE_DIR

LEGACY_TXT_FILE = BASE_DIR / "seen_jobs.txt"

class StorageManager:
    """Handles persistence for seen jobs to prevent duplicate alerts."""

    def __init__(self, json_filepath=SEEN_JOBS_FILE):
        self.filepath = Path(json_filepath)
        self.seen_data = self._load()

    def _load(self):
        """Loads seen job hashes/URLs from JSON with fallback to legacy TXT file."""
        seen = {}
        
        # Load from legacy seen_jobs.txt if exists
        if LEGACY_TXT_FILE.exists():
            try:
                with open(LEGACY_TXT_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        url = line.strip()
                        if url:
                            url_hash = self.generate_hash(url)
                            seen[url_hash] = {
                                "url": url,
                                "added_at": datetime.now(timezone.utc).isoformat()
                            }
            except Exception as e:
                print(f"[Storage] Warning reading legacy txt file: {e}")

        # Load from primary seen_jobs.json
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        seen.update(data)
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, str):
                                h = self.generate_hash(item)
                                seen[h] = {"url": item, "added_at": datetime.now(timezone.utc).isoformat()}
            except Exception as e:
                print(f"[Storage] Error loading {self.filepath}: {e}")

        return seen

    @staticmethod
    def generate_hash(identifier: str) -> str:
        """Generates a stable MD5 hash for a job URL or identifier."""
        return hashlib.md5(identifier.strip().lower().encode("utf-8")).hexdigest()

    def is_seen(self, identifier: str) -> bool:
        """Checks if a job URL or identifier has already been alerted."""
        h = self.generate_hash(identifier)
        return h in self.seen_data

    def add_job(self, identifier: str, title: str = "", source: str = "", pub_date: str = "", company: str = "", matched_keywords: list = None):
        """Adds a job to the seen data store with actual publication date."""
        h = self.generate_hash(identifier)
        self.seen_data[h] = {
            "url": identifier,
            "title": title,
            "source": source,
            "company": company,
            "pub_date": pub_date,
            "matched_keywords": matched_keywords or [],
            "added_at": pub_date if pub_date else datetime.now(timezone.utc).isoformat()
        }

    def save(self):
        """Persists seen jobs to JSON file and legacy TXT file for compatibility."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.seen_data, f, indent=2, ensure_ascii=False)
            
            # Write to legacy TXT file as well to support existing scripts/workflows
            with open(LEGACY_TXT_FILE, "w", encoding="utf-8") as f:
                for item in self.seen_data.values():
                    f.write(f"{item.get('url')}\n")
        except Exception as e:
            print(f"[Storage] Error saving seen jobs: {e}")
