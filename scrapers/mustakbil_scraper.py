from typing import List
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, Job

class MustakbilScraper(BaseScraper):
    """Scraper for Mustakbil.com (Pakistani Tech Job Portal)."""

    SEARCH_KEYWORDS = ["ASO", "App Store", "Mobile Growth", "App Publishing", "User Acquisition"]

    def __init__(self):
        super().__init__("Mustakbil.com Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        for kw in self.SEARCH_KEYWORDS:
            url = f"https://www.mustakbil.com/jobs?q={kw}&location=Pakistan"
            res = self.fetch(url, timeout=4)
            if not res:
                continue

            try:
                soup = BeautifulSoup(res.text, "html.parser")
                job_items = soup.select(".job-item") or soup.select(".job-list-item") or soup.select("article")

                for item in job_items:
                    title_elem = item.select_one("h2 a") or item.select_one("h3 a") or item.select_one("a.job-title")
                    if not title_elem:
                        continue

                    title = title_elem.text.strip()
                    href = title_elem.get("href", "")

                    if not href.startswith("http"):
                        link = f"https://www.mustakbil.com{href}" if href.startswith("/") else f"https://www.mustakbil.com/{href}"
                    else:
                        link = href

                    comp_elem = item.select_one(".company-name") or item.select_one(".company")
                    company = comp_elem.text.strip() if comp_elem else "Mustakbil Employer"

                    loc_elem = item.select_one(".location")
                    location = loc_elem.text.strip() if loc_elem else "Pakistan"

                    date_elem = item.select_one(".date") or item.select_one("time") or item.select_one(".posted-date")
                    pub_date = date_elem.text.strip() if date_elem else ""

                    if title and link:
                        found_jobs.append(
                            Job(
                                title=title,
                                link=link,
                                source="Mustakbil.com (Pakistan)",
                                company=company,
                                location=location,
                                pub_date=pub_date
                            )
                        )
            except Exception as e:
                print(f"[{self.name}] Error scraping keyword '{kw}': {e}")

        print(f"[{self.name}] Total parsed from Mustakbil.com: {len(found_jobs)}")
        return found_jobs
