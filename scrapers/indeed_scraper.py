from typing import List
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, Job

class IndeedPKScraper(BaseScraper):
    """Scraper for Indeed Pakistan (pk.indeed.com)."""

    SEARCH_QUERIES = [
        "ASO",
        "App Store Optimization",
        "App Growth",
        "Play Store Manager",
        "User Acquisition"
    ]

    def __init__(self):
        super().__init__("Indeed Pakistan Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        for q in self.SEARCH_QUERIES:
            formatted_q = q.replace(" ", "+")
            url = f"https://pk.indeed.com/jobs?q={formatted_q}&l=Pakistan"
            res = self.fetch(url, timeout=4)
            if not res:
                continue

            try:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.select(".job_seen_beacon") or soup.select(".jobCard") or soup.select(".result")

                for card in cards:
                    # Title & Link
                    title_elem = card.select_one("h2.jobTitle span") or card.select_one("h2.jobTitle a") or card.select_one("a.jcs-JobTitle")
                    link_elem = card.select_one("a.jcs-JobTitle") or card.select_one("h2.jobTitle a") or card.select_one("a")

                    if not title_elem or not link_elem:
                        continue

                    title = title_elem.text.strip()
                    href = link_elem.get("href", "")

                    if href.startswith("/"):
                        link = f"https://pk.indeed.com{href}"
                    elif not href.startswith("http"):
                        link = f"https://pk.indeed.com/{href}"
                    else:
                        link = href

                    # Company & Location
                    comp_elem = card.select_one("[data-testid='company-name']") or card.select_one(".companyName")
                    company = comp_elem.text.strip() if comp_elem else "Indeed Employer"

                    loc_elem = card.select_one("[data-testid='text-location']") or card.select_one(".companyLocation")
                    location = loc_elem.text.strip() if loc_elem else "Pakistan"

                    snippet_elem = card.select_one(".job-snippet") or card.select_one(".underCardSummary")
                    description = snippet_elem.text.strip() if snippet_elem else ""

                    if title and link:
                        found_jobs.append(
                            Job(
                                title=title,
                                link=link,
                                source="Indeed Pakistan",
                                company=company,
                                location=location,
                                description=description
                            )
                        )
            except Exception as e:
                print(f"[{self.name}] Error scraping query '{q}': {e}")

        print(f"[{self.name}] Total parsed from Indeed PK: {len(found_jobs)}")
        return found_jobs
