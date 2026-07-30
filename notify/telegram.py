import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def escape_markdown(text: str) -> str:
    """Escapes Markdown V1 characters to prevent parsing errors."""
    if not text:
        return ""
    # Standard Markdown special chars: *, _, [, ], (
    chars_to_escape = ["*", "_", "`", "[", "]"]
    for char in chars_to_escape:
        text = text.replace(char, f"\\{char}")
    return text

def send_telegram_alert(title: str, link: str, source: str, matched_keywords: list = None, company: str = "") -> bool:
    """Sends a formatted Telegram message for a single matching job listing."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        # Silently skip if Telegram credentials are not set up
        return False

    kw_str = f"\n🔑 *Keywords:* `{', '.join(matched_keywords)}`" if matched_keywords else ""
    company_str = f"\n🏢 *Company:* {escape_markdown(company)}" if company else ""

    message = (
        f"🎯 *New Job Alert ({escape_markdown(source)})*\n\n"
        f"📌 *Role:* {escape_markdown(title)}"
        f"{company_str}"
        f"{kw_str}\n\n"
        f"🔗 [Apply Here]({link})"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[Telegram] Sent alert: {title} ({source})")
            return True
        else:
            print(f"[Telegram] Error response ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"[Telegram] Failed to send message for {title}: {e}")
        return False

def send_telegram_batch(jobs: list, delay_between_messages: float = 1.0):
    """Sends a batch of job alerts with rate limiting delay."""
    success_count = 0
    for job in jobs:
        title = job.get("title", "Job Listing")
        link = job.get("link", "")
        source = job.get("source", "Job Search")
        matched_kw = job.get("matched_keywords", [])
        company = job.get("company", "")
        
        if send_telegram_alert(title, link, source, matched_kw, company):
            success_count += 1
            time.sleep(delay_between_messages)
    return success_count
