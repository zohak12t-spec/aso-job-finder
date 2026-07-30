import urllib.parse
from typing import List
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, Job

class LinkedInScraper(BaseScraper):
    """
    High-Priority Direct Guest API Scraper for LinkedIn Jobs.
    Fetches real-time LinkedIn listings for Rawalpindi/Islamabad, Pakistan, and Global Remote.
    """

    SEARCH_CONFIGS = [
        {"keywords": "ASO", "location": "Islamabad"},
        {"keywords": "ASO Specialist", "location": "Pakistan"},
        {"keywords": "App Store Optimization", "location": "Pakistan"},
        {"keywords": "App Growth Manager", "location": "Remote"},
        {"keywords": "Play Store Manager", "location": "Pakistan"},
        {"keywords": "User Acquisition Manager", "location": "Remote"},
        {"keywords": "App Monetization Specialist", "location": "Remote"},
        {"keywords": "App Publisher", "location": "Pakistan"}
    ]

    def __init__(self):
        super().__init__("LinkedIn High-Priority Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        headers = self.get_random_headers()
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

        for config in self.SEARCH_CONFIGS:
            kw = config["keywords"]
            loc = config["location"]
            
            # LinkedIn Public Guest Search API URL
            encoded_kw = urllib.parse.quote(kw)
            encoded_loc = urllib.parse.quote(loc)
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_kw}&location={encoded_loc}&start=0"

            res = self.fetch(url, headers=headers, timeout=6)
            if not res or res.status_code != 200:
                continue

            try:
                soup = BeautifulSoup(res.text, "html.parser")
                job_cards = soup.select("li")

                for card in job_cards:
                    title_elem = card.select_one(".base-search-card__title") or card.select_one("h3")
                    link_elem = card.select_one("a.base-card__full-link") or card.select_one("a")
                    comp_elem = card.select_one(".base-search-card__subtitle") or card.select_one("h4")
                    loc_elem = card.select_one(".job-search-card__location")

                    if not title_elem or not link_elem:
                        continue

                    title = title_elem.text.strip()
                    link = link_elem.get("href", "").split("?")[0] # Clean tracking query params
                    company = comp_elem.text.strip() if comp_elem else "LinkedIn Employer"
                    location = loc_elem.text.strip() if loc_elem else loc

                    if title and link and "linkedin.com/jobs" in link:
                        found_jobs.append(
                            Job(
                                title=title,
                                link=link,
                                source=f"LinkedIn ({loc})",
                                company=company,
                                location=location,
                                description=f"Position: {title} | Location: {location}"
                            )
                        )
            except Exception as e:
                print(f"[{self.name}] Error parsing LinkedIn for '{kw}' in '{loc}': {e}")

        print(f"[{self.name}] Total parsed from LinkedIn: {len(found_jobs)}")
        return found_jobs
