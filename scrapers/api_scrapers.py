from typing import List
from scrapers.base import BaseScraper, Job

class APIScraper(BaseScraper):
    """Scrapes remote platforms via public JSON endpoints."""

    def __init__(self):
        super().__init__("JSON API Scraper")

    def fetch_remoteok(self) -> List[Job]:
        jobs = []
        url = "https://remoteok.com/api"
        res = self.fetch(url)
        if res:
            try:
                data = res.json()
                # RemoteOK returns array where first element is legal/meta info
                for item in data:
                    if isinstance(item, dict) and "position" in item:
                        title = item.get("position", "")
                        link = item.get("url", "") or f"https://remoteok.com/remote-jobs/{item.get('id', '')}"
                        company = item.get("company", "RemoteOK")
                        description = item.get("description", "")
                        location = item.get("location", "Remote")
                        pub_date = item.get("date", "")
                        
                        if title and link:
                            jobs.append(
                                Job(
                                    title=title,
                                    link=link,
                                    source="RemoteOK",
                                    company=company,
                                    location=location,
                                    description=description,
                                    pub_date=str(pub_date)
                                )
                            )
            except Exception as e:
                print(f"[{self.name}] Error parsing RemoteOK API: {e}")
        return jobs

    def fetch_remotive_api(self) -> List[Job]:
        jobs = []
        categories = ["marketing", "product", "business"]
        for cat in categories:
            url = f"https://remotive.com/api/remote-jobs?category={cat}&limit=50"
            res = self.fetch(url)
            if res:
                try:
                    data = res.json()
                    for item in data.get("jobs", []):
                        title = item.get("title", "")
                        link = item.get("url", "")
                        company = item.get("company_name", "")
                        description = item.get("description", "")
                        pub_date = item.get("publication_date", "")
                        
                        if title and link:
                            jobs.append(
                                Job(
                                    title=title,
                                    link=link,
                                    source="Remotive API",
                                    company=company,
                                    location="Remote",
                                    description=description,
                                    pub_date=pub_date
                                )
                            )
                except Exception as e:
                    print(f"[{self.name}] Error parsing Remotive category {cat}: {e}")
        return jobs

    def run(self) -> List[Job]:
        all_jobs = []
        all_jobs.extend(self.fetch_remoteok())
        all_jobs.extend(self.fetch_remotive_api())
        print(f"[{self.name}] Total parsed from APIs: {len(all_jobs)}")
        return all_jobs
