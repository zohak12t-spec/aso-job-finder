import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from config import KEYWORDS, MAX_CONCURRENT_SCRAPERS
from storage import StorageManager
from notify import send_telegram_batch, send_email_digest, generate_reports
from scrapers import ALL_SCRAPERS, Job

class JobAutomationEngine:
    """Orchestrates scraping, keyword matching, deduplication, and multi-format output generation."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.storage = StorageManager()
        self.keywords = [k.lower().strip() for k in KEYWORDS]

    def match_job(self, job: Job) -> bool:
        """Evaluates whether job title or description matches the keyword matrix using word boundaries."""
        text_to_search = f"{job.title} {job.description}".lower()
        matched = []

        for kw in self.keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_to_search):
                matched.append(kw)

        if matched:
            job.matched_keywords = list(set(matched))
            return True
        return False

    def run_scraper_instance(self, scraper_cls) -> List[Job]:
        """Instantiates and executes a scraper safely within a try-except block."""
        try:
            instance = scraper_cls()
            print(f"[Engine] Starting {instance.name}...")
            jobs = instance.run()
            print(f"[Engine] Completed {instance.name} (Found {len(jobs)} total jobs)")
            return jobs
        except Exception as e:
            print(f"[Engine] Scraper {scraper_cls.__name__} failed: {e}")
            return []

    def execute(self) -> Dict[str, Any]:
        """Runs the complete automation cycle."""
        start_time = time.time()
        print("==================================================")
        print("[START] STARTING MULTI-PLATFORM JOB AUTOMATION ENGINE")
        print("==================================================")

        all_raw_jobs: List[Job] = []

        # Step 1: Run scrapers concurrently
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_SCRAPERS) as executor:
            future_to_scraper = {executor.submit(self.run_scraper_instance, cls): cls for cls in ALL_SCRAPERS}
            for future in as_completed(future_to_scraper):
                res = future.result()
                if res:
                    all_raw_jobs.extend(res)

        print(f"\n[Engine] Total Raw Jobs Scraped Across All Platforms: {len(all_raw_jobs)}")

        # Step 2: Keyword Matching & Deduplication
        matched_jobs: List[Job] = []
        new_unseen_jobs: List[Job] = []

        for job in all_raw_jobs:
            if not job.link or not job.title:
                continue

            if self.match_job(job):
                matched_jobs.append(job)
                
                # Check storage deduplication
                if not self.storage.is_seen(job.link):
                    new_unseen_jobs.append(job)

        print(f"[Engine] Total Matched Jobs (Keyword Matrix): {len(matched_jobs)}")
        print(f"[Engine] New Unseen Jobs To Process: {len(new_unseen_jobs)}")

        # Ensure web dashboard receives ALL matched jobs + stored history
        all_matched_dicts = [j.to_dict() for j in matched_jobs]
        stored_jobs_map = self.storage.seen_data
        existing_urls = {j.get("link") or j.get("url") for j in all_matched_dicts if (j.get("link") or j.get("url"))}
        
        for job_hash, item in stored_jobs_map.items():
            url = item.get("url") or item.get("link")
            if url and url not in existing_urls:
                all_matched_dicts.append({
                    "title": item.get("title", "Saved Role"),
                    "link": url,
                    "url": url,
                    "company": item.get("company", "Direct Employer"),
                    "source": item.get("source", "Portal"),
                    "matched_keywords": item.get("matched_keywords", ["ASO", "App Growth"]),
                    "added_at": item.get("added_at")
                })

        new_job_dicts = [j.to_dict() for j in new_unseen_jobs]

        # Step 3: Generate Local File Outputs (HTML Dashboard & Markdown Report)
        if not self.dry_run:
            print(f"\n[Engine] Generating Local & Cloudflare File Outputs ({len(all_matched_dicts)} total active jobs)...")
            generate_reports(all_matched_dicts)

            # Optional Telegram Sending (only for new unseen jobs)
            print("\n[Engine] Checking Optional Telegram Alerts...")
            send_telegram_batch(new_job_dicts)

            # Optional Email Digest Sending
            send_email_digest(new_job_dicts)

            # Save seen state
            for job in new_unseen_jobs:
                self.storage.add_job(job.link, title=job.title, source=job.source)
            self.storage.save()
        else:
            print(f"\n[DRY RUN] Generating Local File Outputs Preview ({len(all_matched_dicts)} total jobs)...")
            generate_reports(all_matched_dicts)

        # Print Terminal Table / List Output
        print("\n" + "="*80)
        print("🎯 NEW MATCHING JOBS SUMMARY")
        print("="*80)
        if new_unseen_jobs:
            for idx, j in enumerate(new_unseen_jobs, 1):
                kws = ", ".join(j.matched_keywords)
                print(f" {idx:2d}. [{j.source}] {j.title}")
                print(f"     Company: {j.company} | Matches: {kws}")
                print(f"     Link: {j.link}\n")
        else:
            print(" No new matching jobs found since last run.")

        elapsed = round(time.time() - start_time, 2)
        print("==================================================")
        print(f"[SUCCESS] EXECUTION COMPLETED IN {elapsed} SECONDS")
        print(f"   Raw Jobs Scraped : {len(all_raw_jobs)}")
        print(f"   Matches Found    : {len(matched_jobs)}")
        print(f"   New Jobs Processed: {len(new_unseen_jobs)}")
        print(f"   Dashboard Saved  : jobs_report.html")
        print(f"   CSV File Saved   : matched_jobs.csv")
        print("==================================================")

        return {
            "elapsed_seconds": elapsed,
            "raw_jobs_count": len(all_raw_jobs),
            "matched_count": len(matched_jobs),
            "new_jobs_count": len(new_unseen_jobs)
        }
