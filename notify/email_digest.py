import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import (
    ENABLE_EMAIL_DIGEST,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS,
    EMAIL_RECIPIENT
)

def send_email_digest(jobs: list) -> bool:
    """Sends an HTML formatted summary email containing all new matching job listings."""
    if not ENABLE_EMAIL_DIGEST:
        print("[Email] Email digest is disabled in config/environment.")
        return False

    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_RECIPIENT]):
        print("[Email] Missing SMTP configuration. Please check environment variables.")
        return False

    if not jobs:
        print("[Email] No new jobs to send in digest.")
        return False

    date_str = datetime.now().strftime("%B %d, %Y")
    subject = f"🎯 Job Digest Alert ({len(jobs)} New Roles) - {date_str}"

    # Build HTML Content
    job_rows = ""
    for j in jobs:
        title = j.get("title", "Untitled Job")
        link = j.get("link", "#")
        source = j.get("source", "Unknown Platform")
        company = j.get("company", "N/A")
        matched = ", ".join(j.get("matched_keywords", []))

        job_rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px; font-family: sans-serif;">
                <strong style="font-size: 16px; color: #1a0dab;">
                    <a href="{link}" target="_blank" style="text-decoration: none; color: #1a0dab;">{title}</a>
                </strong>
                <div style="font-size: 13px; color: #555; margin-top: 4px;">
                    🏢 <strong>Company:</strong> {company} | 📌 <strong>Platform:</strong> <span style="background: #e8f0fe; color: #1a73e8; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{source}</span>
                </div>
                {f'<div style="font-size: 12px; color: #28a745; margin-top: 4px;">🔑 <strong>Matched Keywords:</strong> {matched}</div>' if matched else ''}
            </td>
            <td style="padding: 12px; text-align: right;">
                <a href="{link}" target="_blank" style="background-color: #007bff; color: white; padding: 8px 14px; text-decoration: none; border-radius: 4px; font-size: 13px; font-weight: bold; display: inline-block;">Apply Now</a>
            </td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Daily Job Digest</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px;">
        <table align="center" width="650" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-collapse: collapse;">
            <thead>
                <tr style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white;">
                    <th colspan="2" style="padding: 24px; text-align: left;">
                        <h2 style="margin: 0; font-size: 22px;">🎯 New Job Listings Digest</h2>
                        <p style="margin: 6px 0 0 0; opacity: 0.85; font-weight: normal; font-size: 14px;">Found {len(jobs)} matching opportunities on {date_str}</p>
                    </th>
                </tr>
            </thead>
            <tbody>
                {job_rows}
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2" style="padding: 16px; background-color: #fafafa; text-align: center; color: #888; font-size: 12px;">
                        Automated Python Job Alert System • Powered by Antigravity Engine
                    </td>
                </tr>
            </tfoot>
        </table>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_RECIPIENT
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, EMAIL_RECIPIENT, msg.as_string())
        print(f"[Email] Successfully sent digest with {len(jobs)} jobs to {EMAIL_RECIPIENT}.")
        return True
    except Exception as e:
        print(f"[Email] Failed to send email digest: {e}")
        return False
