import random
import requests
from dataclasses import dataclass, field
from typing import List, Optional
from config import USER_AGENTS, DEFAULT_TIMEOUT

@dataclass
class Job:
    title: str
    link: str
    source: str
    company: str = ""
    location: str = ""
    description: str = ""
    pub_date: str = ""
    matched_keywords: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "pub_date": self.pub_date,
            "matched_keywords": self.matched_keywords
        }

class BaseScraper:
    """Abstract base class for job scrapers."""

    def __init__(self, name: str):
        self.name = name

    def get_random_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache"
        }

    def fetch(self, url: str, headers: Optional[dict] = None, timeout: int = DEFAULT_TIMEOUT) -> Optional[requests.Response]:
        """Performs HTTP GET with error handling and custom headers."""
        if not headers:
            headers = self.get_random_headers()
        try:
            res = requests.get(url, headers=headers, timeout=timeout)
            res.raise_for_status()
            return res
        except Exception as e:
            print(f"[{self.name}] Error fetching {url}: {e}")
            return None

    def run(self) -> List[Job]:
        raise NotImplementedError("Scrapers must implement the run() method.")
