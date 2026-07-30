# 🎯 Professional Multi-Platform Job Search & Telegram Alert System

A production-grade Python automation engine that connects **10+ Pakistani local and international remote job platforms** into a single unified scraper. It scans listings against an exhaustive ASO, App Publishing, User Acquisition (UA), and Mobile Growth keyword matrix, delivers instant Telegram alerts, and maintains duplicate-prevention state.

---

## 🚀 Supported Platforms (10+ Connected)

### 🇵🇰 Pakistani Local & Regional Platforms
1. **Indeed Pakistan (`pk.indeed.com`)**: Scraped directly with fallback CSS selector parsing.
2. **Rozee.pk**: Pakistan’s largest portal, parsed via target search queries (`/job/jsearch/q/...`).
3. **Mustakbil.com**: Pakistani tech portal for software houses and app publishing agencies.
4. **Glassdoor (Pakistan Filter)**: Extracted safely via Google Search index queries.

### 🌐 International Remote & Global Platforms
5. **WeWorkRemotely**: Public RSS feeds (`remote-marketing-jobs.rss`, etc.).
6. **Remotive.com**: Direct official JSON API endpoints (`/api/remote-jobs`) + RSS feed.
7. **Jobspresso**: RSS feed integration for remote growth, marketing, and product roles.
8. **RemoteOK**: Direct JSON API endpoint (`https://remoteok.com/api`).
9. **LinkedIn (Google Search Index Query Scraper)**: Queries Google Search index (`site:linkedin.com/jobs "ASO" "Pakistan" OR "Remote"`) to extract fresh postings safely without anti-bot blocks.

---

## 🔑 Exhaustive Keyword Matrix

Matches job titles and descriptions against the following industry keywords:

- **Core ASO**: `aso`, `app store optimization`, `app store optimizer`, `aso specialist`, `aso manager`, `aso executive`
- **App Publishing & Ops**: `app publisher`, `app publishing`, `app publish manager`, `play store manager`, `app store connect`, `google play console`, `app operations`, `app ops`
- **Growth & Marketing**: `app growth`, `mobile growth`, `mobile marketing`, `mobile app marketer`, `growth marketer`, `app acquisition`
- **User Acquisition & Monetization**: `user acquisition`, `ua manager`, `ua specialist`, `app monetization`, `adops`, `ad operations`, `admob`, `applovin`, `iron source`, `unity ads`
- **Product & Gaming**: `mobile product marketing`, `game publisher`, `game growth manager`

---

## 🛠️ Setup & Installation

### 1. Clone & Install Dependencies

```bash
cd "d:/zohaks_development/demo work/python job script/script"
python -m pip install -r requirements.txt
```

### 2. Configure Environment Variables (`.env`)

Copy `.env.example` to `.env` and fill in your Telegram credentials:

```bash
cp .env.example .env
```

Set your Telegram parameters:
- `TELEGRAM_BOT_TOKEN`: Token from [@BotFather](https://t.me/BotFather)
- `TELEGRAM_CHAT_ID`: Your chat ID or channel ID (get via [@userinfobot](https://t.me/userinfobot))

---

## 🧪 Usage Commands

### 1. Run Dry-Run Mode (Test Scraping & Matching without sending real Telegram alerts)
```bash
python main.py --dry-run
```

### 2. Test Telegram Bot Connection
```bash
python main.py --test-telegram
```

### 3. Test Optional Email Digest
```bash
python main.py --test-email
```

### 4. Run Standard Live Automation
```bash
python main.py
```

### 5. Clear Duplicate History State
```bash
python main.py --reset-seen
```

---

## ⏰ Automated GitHub Actions Setup

This repository includes `.github/workflows/job_scraper.yml` to automatically run every 3 hours and commit updated `seen_jobs.json` to prevent duplicate alerts.

To enable GitHub Actions:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Add the following repository secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - *(Optional)* `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_RECIPIENT`, `ENABLE_EMAIL_DIGEST`
3. Push your repository to GitHub. Workflow will start running automatically!
