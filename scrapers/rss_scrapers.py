import feedparser
from typing import List
from scrapers.base import BaseScraper, Job

class RSSFeedScraper(BaseScraper):
    """Scrapes remote job platforms using public RSS feeds."""

    FEEDS = {
        "WeWorkRemotely": [
            "https://weworkremotely.com/categories/remote-marketing-jobs.rss",
            "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss"
        ],
        "Remotive RSS": [
            "https://remotive.com/remote-jobs/feed/marketing",
            "https://remotive.com/remote-jobs/feed/product"
        ],
        "Jobspresso": [
            "https://jobspresso.co/feed/"
        ]
    }

    def __init__(self):
        super().__init__("RSS Feed Scraper")

    def run(self) -> List[Job]:
        found_jobs: List[Job] = []

        for source_name, feed_urls in self.FEEDS.items():
            for url in feed_urls:
                try:
                    feed = feedparser.parse(url)
                    if not feed or not hasattr(feed, 'entries'):
                        continue
                    
                    for entry in feed.entries:
                        title = getattr(entry, 'title', '').strip()
                        link = getattr(entry, 'link', '').strip()
                        summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                        pub_date = getattr(entry, 'published', '')

                        if title and link:
                            found_jobs.append(
                                Job(
                                    title=title,
                                    link=link,
                                    source=source_name,
                                    company=getattr(entry, 'author', source_name),
                                    description=summary,
                                    pub_date=pub_date
                                )
                            )
                except Exception as e:
                    print(f"[{self.name}] Error parsing feed {url}: {e}")

        print(f"[{self.name}] Total parsed from RSS feeds: {len(found_jobs)}")
        return found_jobs
