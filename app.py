import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from engine import JobAutomationEngine
from storage import StorageManager
from config import BASE_DIR, SEEN_JOBS_FILE

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def index():
    """Serves the Web Dashboard Single Page Application."""
    return render_template("index.html")

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """Returns all saved jobs from history."""
    storage = StorageManager()
    seen_jobs = list(storage.seen_data.values())
    # Sort reverse by added_at
    seen_jobs.sort(key=lambda x: x.get("added_at", ""), reverse=True)
    return jsonify({
        "success": True,
        "count": len(seen_jobs),
        "jobs": seen_jobs
    })

@app.route("/api/scrape", methods=["POST"])
def trigger_scrape():
    """Triggers the live scraping engine across 10+ platforms."""
    try:
        data = request.json or {}
        dry_run = data.get("dry_run", False)

        engine = JobAutomationEngine(dry_run=dry_run)
        results = engine.execute()

        # Load updated jobs list
        storage = StorageManager()
        seen_jobs = list(storage.seen_data.values())
        seen_jobs.sort(key=lambda x: x.get("added_at", ""), reverse=True)

        return jsonify({
            "success": True,
            "metrics": results,
            "jobs": seen_jobs
        })
    except Exception as e:
        print(f"[API Error] Exception during scraping: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/clear-history", methods=["POST"])
def clear_history():
    """Clears saved jobs history."""
    try:
        if SEEN_JOBS_FILE.exists():
            SEEN_JOBS_FILE.unlink()
        legacy_file = BASE_DIR / "seen_jobs.txt"
        if legacy_file.exists():
            legacy_file.unlink()
        return jsonify({"success": True, "message": "History cleared successfully."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    print("==================================================")
    print("[START] STARTING ASO & APP GROWTH JOB SEARCH WEB SERVER")
    print("   Open in your browser: http://localhost:5000")
    print("==================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
