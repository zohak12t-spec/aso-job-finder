from .base import BaseScraper, Job
from .linkedin_scraper import LinkedInScraper
from .rss_scrapers import RSSFeedScraper
from .api_scrapers import APIScraper
from .rozee_scraper import RozeeScraper
from .mustakbil_scraper import MustakbilScraper
from .indeed_scraper import IndeedPKScraper
from .google_scraper import GoogleIndexScraper

ALL_SCRAPERS = [
    LinkedInScraper,  # High priority LinkedIn guest scraper
    RSSFeedScraper,
    APIScraper,
    MustakbilScraper,
    IndeedPKScraper,
    RozeeScraper,
    GoogleIndexScraper
]
