import sys
import argparse
from engine import JobAutomationEngine
from notify.telegram import send_telegram_alert
from notify.email_digest import send_email_digest
from storage import StorageManager
from config import SEEN_JOBS_FILE, BASE_DIR

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Multi-Platform Professional Job Search & Alert Automation System")
    parser.add_argument("--dry-run", action="store_true", help="Run scraping and matching without sending real alerts or updating storage.")
    parser.add_argument("--test-telegram", action="store_true", help="Send a test notification to Telegram to verify configuration.")
    parser.add_argument("--test-email", action="store_true", help="Send a test email digest to verify SMTP configuration.")
    parser.add_argument("--reset-seen", action="store_true", help="Clear the seen jobs history file.")

    args = parser.parse_args()

    if args.reset_seen:
        if SEEN_JOBS_FILE.exists():
            SEEN_JOBS_FILE.unlink()
            print("[CLI] Successfully cleared seen_jobs.json history.")
        legacy_file = BASE_DIR / "seen_jobs.txt"
        if legacy_file.exists():
            legacy_file.unlink()
            print("[CLI] Successfully cleared seen_jobs.txt legacy history.")
        return

    if args.test_telegram:
        print("[CLI] Sending test Telegram notification...")
        success = send_telegram_alert(
            title="Test Role: ASO Specialist & App Growth Manager",
            link="https://github.com",
            source="System Test",
            matched_keywords=["aso", "app growth"],
            company="Antigravity Test Suite"
        )
        if success:
            print("✅ Telegram test successful!")
        else:
            print("❌ Telegram test failed. Check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.")
        return

    if args.test_email:
        print("[CLI] Sending test email digest...")
        test_job = {
            "title": "Test Role: ASO Manager",
            "link": "https://github.com",
            "source": "System Test",
            "company": "Antigravity Corp",
            "matched_keywords": ["aso manager", "app store optimization"]
        }
        success = send_email_digest([test_job])
        if success:
            print("✅ Email digest test successful!")
        else:
            print("❌ Email test failed. Check your SMTP configurations in .env.")
        return

    # Normal Engine Execution
    engine = JobAutomationEngine(dry_run=args.dry_run)
    engine.execute()

if __name__ == "__main__":
    main()
