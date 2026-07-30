from typing import List
from scrapers.base import BaseScraper, Job

class HimalayasScraper(BaseScraper):
    """Scraper for Himalayas.app public JSON endpoint (Global Remote App & Marketing Jobs)."""

    def __init__(self):
        super().__init__("Himalayas Remote API Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []
        headers = self.get_random_headers()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        url = "https://himalayas.app/jobs/api?limit=50"
        res = self.fetch(url, headers=headers, timeout=6)

        if not res or res.status_code != 200:
            return found_jobs

        try:
            data = res.json()
            job_list = data.get("jobs", []) if isinstance(data, dict) else []

            for item in job_list:
                title = item.get("title", "")
                company = item.get("companyName", "Himalayas Employer")
                location = item.get("locationRestriction", "Global Remote")
                link = item.get("applicationUrl") or item.get("url", "")
                pub_date = item.get("pubDate", "")
                description = item.get("excerpt", "")

                if title and link:
                    found_jobs.append(
                        Job(
                            title=title,
                            link=link,
                            source="Himalayas",
                            company=company,
                            location=location,
                            pub_date=str(pub_date),
                            description=description
                        )
                    )
        except Exception as e:
            print(f"[{self.name}] Error parsing Himalayas API: {e}")

        print(f"[{self.name}] Total parsed from Himalayas API: {len(found_jobs)}")
        return found_jobs
