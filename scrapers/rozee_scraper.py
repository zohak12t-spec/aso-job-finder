from typing import List
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, Job

class RozeeScraper(BaseScraper):
    """Scraper for Rozee.pk (Pakistan's largest job portal)."""

    SEARCH_KEYWORDS = [
        "aso", "app-growth", "mobile-marketing", 
        "user-acquisition", "play-store", "app-store"
    ]

    def __init__(self):
        super().__init__("Rozee.pk Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        for kw in self.SEARCH_KEYWORDS:
            url = f"https://www.rozee.pk/job/jsearch/q/{kw}"
            res = self.fetch(url, timeout=4)
            if not res:
                continue

            try:
                soup = BeautifulSoup(res.text, "html.parser")
                # Parse job cards
                job_cards = soup.select(".job") or soup.select(".job-card") or soup.select("div[id^='job_']")
                
                for card in job_cards:
                    # Title & Link extraction
                    title_elem = card.select_one(".jtitle a") or card.select_one(".title a") or card.select_one("h3 a")
                    if not title_elem:
                        continue

                    title = title_elem.text.strip()
                    href = title_elem.get("href", "")
                    
                    if not href.startswith("http"):
                        link = f"https://www.rozee.pk{href}" if href.startswith("/") else f"https://www.rozee.pk/{href}"
                    else:
                        link = href

                    # Company extraction
                    comp_elem = card.select_one(".cname") or card.select_one(".company") or card.select_one(".c-name")
                    company = comp_elem.text.strip() if comp_elem else "Rozee Employer"

                    # Location extraction
                    loc_elem = card.select_one(".loc") or card.select_one(".location")
                    location = loc_elem.text.strip() if loc_elem else "Pakistan"

                    # Description snippet
                    desc_elem = card.select_one(".jdesc") or card.select_one(".description")
                    description = desc_elem.text.strip() if desc_elem else ""

                    if title and link:
                        found_jobs.append(
                            Job(
                                title=title,
                                link=link,
                                source="Rozee.pk (Pakistan)",
                                company=company,
                                location=location,
                                description=description
                            )
                        )
            except Exception as e:
                print(f"[{self.name}] Error scraping keyword '{kw}': {e}")

        print(f"[{self.name}] Total parsed from Rozee.pk: {len(found_jobs)}")
        return found_jobs
