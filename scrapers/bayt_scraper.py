import urllib.parse
from typing import List
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, Job

class BaytScraper(BaseScraper):
    """Scraper for Bayt.com Middle East & Pakistan Jobs via DuckDuckGo Index fallback."""

    QUERIES = [
        "site:bayt.com/en/pakistan/jobs ASO",
        "site:bayt.com/en/pakistan/jobs App Store Optimization",
        "site:bayt.com/en/pakistan/jobs App Growth Manager",
        "site:bayt.com/en/pakistan/jobs User Acquisition"
    ]

    def __init__(self):
        super().__init__("Bayt.com Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []
        headers = self.get_random_headers()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

        for query in self.QUERIES:
            encoded = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            res = self.fetch(url, headers=headers, timeout=5)

            if not res or res.status_code != 200:
                continue

            try:
                soup = BeautifulSoup(res.text, "html.parser")
                results = soup.select(".result")

                for r in results:
                    title_a = r.select_one(".result__title a")
                    snippet_div = r.select_one(".result__snippet")

                    if not title_a:
                        continue

                    title = title_a.text.strip()
                    link = title_a.get("href", "")
                    snippet = snippet_div.text.strip() if snippet_div else ""

                    if "uddg=" in link:
                        parsed_link = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("uddg")
                        if parsed_link:
                            link = parsed_link[0]

                    if title and link and "bayt.com" in link.lower():
                        found_jobs.append(
                            Job(
                                title=title.replace("- Bayt.com", "").strip(),
                                link=link,
                                source="Bayt.com (Pakistan)",
                                company="Bayt Employer",
                                location="Pakistan / Middle East",
                                description=snippet
                            )
                        )
            except Exception as e:
                print(f"[{self.name}] Error scraping Bayt for query '{query}': {e}")

        print(f"[{self.name}] Total parsed from Bayt.com: {len(found_jobs)}")
        return found_jobs
