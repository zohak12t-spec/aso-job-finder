import urllib.parse
import requests
from typing import List
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.base import BaseScraper, Job

class GoogleIndexScraper(BaseScraper):
    """
    Scrapes Google and DuckDuckGo Search index to safely extract fresh LinkedIn, 
    Glassdoor, Indeed PK, and Rozee.pk job postings without anti-bot blocks.
    """

    SEARCH_QUERIES = [
        {"source": "LinkedIn Jobs", "query": 'site:linkedin.com/jobs "ASO" OR "App Store Optimization" "Pakistan"'},
        {"source": "LinkedIn Remote", "query": 'site:linkedin.com/jobs "ASO" OR "App Publisher" "Remote"'},
        {"source": "Glassdoor PK", "query": 'site:glassdoor.com "ASO" OR "App Store Optimization" Pakistan'}
    ]

    def __init__(self):
        super().__init__("Search Index Scraper (LinkedIn/Glassdoor)")

    def scrape_single_query(self, item: dict) -> List[Job]:
        jobs = []
        source_label = item["source"]
        q = item["query"]

        # Fast DuckDuckGo search
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
            headers = self.get_random_headers()
            res = requests.get(url, headers=headers, timeout=4)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                results = soup.select(".result")
                for r in results:
                    title_elem = r.select_one(".result__title a")
                    snippet_elem = r.select_one(".result__snippet")
                    if title_elem:
                        title = title_elem.text.strip()
                        href = title_elem.get("href", "")
                        if "uddg=" in href:
                            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                            link = parsed.get("uddg", [href])[0]
                        else:
                            link = href

                        snippet = snippet_elem.text.strip() if snippet_elem else ""

                        if link and ("linkedin.com" in link or "glassdoor.com" in link or "rozee.pk" in link or "indeed.com" in link):
                            jobs.append(
                                Job(
                                    title=title,
                                    link=link,
                                    source=source_label,
                                    company="Search Index Result",
                                    description=snippet
                                )
                            )
        except Exception as e:
            pass
        return jobs

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.scrape_single_query, item) for item in self.SEARCH_QUERIES]
            for future in as_completed(futures):
                res = future.result()
                if res:
                    found_jobs.extend(res)

        print(f"[{self.name}] Total parsed from Search Index: {len(found_jobs)}")
        return found_jobs
