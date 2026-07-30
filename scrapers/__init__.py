from .base import BaseScraper, Job
from .linkedin_scraper import LinkedInScraper
from .bayt_scraper import BaytScraper
from .glassdoor_scraper import GlassdoorScraper
from .himalayas_scraper import HimalayasScraper
from .rss_scrapers import RSSFeedScraper
from .api_scrapers import APIScraper
from .mustakbil_scraper import MustakbilScraper
from .rozee_scraper import RozeeScraper
from .indeed_scraper import IndeedPKScraper
from .google_scraper import GoogleIndexScraper

ALL_SCRAPERS = [
    LinkedInScraper,    # High priority LinkedIn guest scraper
    BaytScraper,        # Bayt.com Middle East & Pakistan portal
    GlassdoorScraper,   # Glassdoor & DuckDuckGo Index scraper
    HimalayasScraper,   # Himalayas.app remote JSON API
    MustakbilScraper,   # Mustakbil.com Pakistani tech portal
    RSSFeedScraper,     # WeWorkRemotely & Remotive RSS
    APIScraper,         # RemoteOK & Remotive API
    IndeedPKScraper,
    RozeeScraper,
    GoogleIndexScraper
]
