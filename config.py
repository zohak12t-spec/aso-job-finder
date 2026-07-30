import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if available
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Email Settings
ENABLE_EMAIL_DIGEST = os.getenv("ENABLE_EMAIL_DIGEST", "false").lower() == "true"
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")

# Storage Settings
SEEN_JOBS_FILE = BASE_DIR / "seen_jobs.json"
JOBS_HISTORY_FILE = BASE_DIR / "jobs_history.json"

# Exhaustive Keyword Matrix tailored for ASO & Mobile App Growth Professional (4-5 YOE)
KEYWORDS = [
    # Core ASO Titles & Skills
    "aso", "app store optimization", "app store optimizer", 
    "aso specialist", "aso manager", "aso executive",
    
    # App Publishing, Console Ops & Search Console
    "app publisher", "app publishing", "app publish manager",
    "play store manager", "app store connect", "google play console",
    "google search console", "app operations", "app ops", "android app marketer",
    
    # Growth & Marketing Titles
    "app growth", "app growth manager", "mobile growth", "mobile marketing", 
    "mobile app marketer", "growth marketer", "app acquisition",
    
    # User Acquisition, Ad Placement & Monetization
    "user acquisition", "ua manager", "ua specialist",
    "app monetization", "admob", "ads placement", "ad placement",
    "adops", "ad operations", "applovin", "ironsource", "unity ads",
    
    # Product & Gaming Ops
    "mobile product marketing", "game publisher", "game growth manager"
]

# Scraping Headers & User Agents Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]

DEFAULT_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "8"))
MAX_CONCURRENT_SCRAPERS = int(os.getenv("MAX_CONCURRENT_SCRAPERS", "5"))
