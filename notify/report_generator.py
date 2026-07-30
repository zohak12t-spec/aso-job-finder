import json
from datetime import datetime
from pathlib import Path
from config import BASE_DIR

DIST_DIR = BASE_DIR / "dist"
REPORTS_DIR = BASE_DIR / "reports"

def generate_reports(jobs: list) -> tuple:
    """
    Generates local jobs_report.html/md and standalone dist/index.html 
    for 100% free Cloudflare Pages static web hosting.
    """
    DIST_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    
    html_path = REPORTS_DIR / "jobs_report.html"
    md_path = REPORTS_DIR / "jobs_report.md"
    dist_html_path = DIST_DIR / "index.html"

    # Convert jobs list to JSON string for embedding
    jobs_json_embedded = json.dumps(jobs, indent=2, ensure_ascii=False)

    # Standalone HTML Dashboard for Cloudflare Pages
    dist_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASO & App Growth Jobs</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-surface: #111827;
            --bg-card: #1f2937;
            --bg-card-hover: #263346;
            --border-subtle: #374151;
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --text-tertiary: #6b7280;
            --brand-blue: #2563eb;
            --brand-blue-hover: #1d4ed8;
            --font-family: 'Inter', 'Plus Jakarta Sans', sans-serif;
            --radius-md: 10px;
            --radius-lg: 14px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; text-transform: none !important; }}
        body {{ background-color: var(--bg-main); color: var(--text-primary); font-family: var(--font-family); min-height: 100vh; line-height: 1.5; }}
        .app-header {{ background-color: var(--bg-surface); border-bottom: 1px solid var(--border-subtle); padding: 20px 0; }}
        .header-container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; display: flex; justify-content: space-between; align-items: center; gap: 20px; }}
        .brand {{ display: flex; align-items: center; gap: 14px; }}
        .brand-logo {{ width: 42px; height: 42px; background-color: rgba(37, 99, 235, 0.12); border: 1px solid rgba(37, 99, 235, 0.3); color: var(--brand-blue); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; }}
        .brand-text h2 {{ font-size: 20px; font-weight: 600; color: var(--text-primary); }}
        .brand-text p {{ font-size: 13px; color: var(--text-secondary); }}
        .main-content {{ max-width: 1200px; width: 100%; margin: 0 auto; padding: 32px 24px 60px 24px; }}
        .toolbar-panel {{ background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 20px; }}
        .toolbar-left, .toolbar-right {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
        .tab-group {{ display: flex; background-color: var(--bg-main); padding: 4px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); }}
        .tab-item {{ background: transparent; border: none; color: var(--text-secondary); font-family: var(--font-family); font-size: 13px; font-weight: 500; padding: 7px 14px; border-radius: 6px; cursor: pointer; }}
        .tab-item.active {{ background-color: var(--bg-card); color: var(--text-primary); font-weight: 600; }}
        .select-input {{ background-color: var(--bg-main); border: 1px solid var(--border-subtle); color: var(--text-primary); font-family: var(--font-family); font-size: 13px; padding: 8px 12px; border-radius: var(--radius-md); outline: none; }}
        .search-input-box {{ display: flex; align-items: center; gap: 8px; background-color: var(--bg-main); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 8px 14px; width: 260px; color: var(--text-tertiary); }}
        .search-input-box input {{ background: transparent; border: none; outline: none; color: var(--text-primary); font-family: var(--font-family); font-size: 13px; width: 100%; }}
        .tags-filter-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 28px; flex-wrap: wrap; }}
        .chip-item {{ background-color: var(--bg-surface); border: 1px solid var(--border-subtle); color: var(--text-secondary); font-family: var(--font-family); font-size: 12px; padding: 5px 12px; border-radius: 20px; cursor: pointer; }}
        .chip-item.active {{ background-color: rgba(37, 99, 235, 0.15); border-color: rgba(37, 99, 235, 0.4); color: #60a5fa; font-weight: 600; }}
        .results-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}
        .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }}
        .job-card {{ background-color: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 22px; display: flex; flex-direction: column; justify-content: space-between; }}
        .job-card:hover {{ background-color: var(--bg-card-hover); border-color: var(--border-highlight); }}
        .source-tag {{ display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; background-color: rgba(37, 99, 235, 0.15); color: #60a5fa; margin-bottom: 12px; }}
        .job-title {{ font-size: 17px; font-weight: 600; line-height: 1.35; margin-bottom: 10px; }}
        .job-title a {{ color: var(--text-primary); text-decoration: none; }}
        .meta-row {{ display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }}
        .skills-list {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }}
        .skill-badge {{ background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); color: #d1d5db; font-size: 11px; padding: 2px 8px; border-radius: 4px; }}
        .card-footer {{ padding-top: 16px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; }}
        .date-text {{ font-size: 12px; color: var(--text-tertiary); }}
        .btn-apply {{ display: inline-flex; align-items: center; gap: 6px; background-color: rgba(37, 99, 235, 0.12); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.3); padding: 7px 14px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600; }}
        .btn-apply:hover {{ background-color: var(--brand-blue); color: #ffffff; }}
        .app-footer {{ text-align: center; padding: 24px; font-size: 13px; color: var(--text-tertiary); border-top: 1px solid var(--border-subtle); }}
    </style>
</head>
<body>
    <div class="app-layout">
        <header class="app-header">
            <div class="header-container">
                <div class="brand">
                    <div class="brand-logo">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                    </div>
                    <div class="brand-text">
                        <h2>ASO & App Growth Jobs</h2>
                        <p>Curated roles for Islamabad, Rawalpindi, and Remote</p>
                    </div>
                </div>
            </div>
        </header>

        <main class="main-content">
            <div class="toolbar-panel">
                <div class="toolbar-left">
                    <div class="tab-group">
                        <button class="tab-item active" data-tab="all">All Jobs</button>
                        <button class="tab-item" data-tab="local">Islamabad & Rawalpindi</button>
                        <button class="tab-item" data-tab="remote">Remote Roles</button>
                    </div>
                </div>
                <div class="toolbar-right">
                    <div class="select-wrapper">
                        <select id="dateFilter" class="select-input">
                            <option value="all">All Timeframes</option>
                            <option value="1">Past 24 Hours</option>
                            <option value="3">Past 3 Days</option>
                            <option value="7">Past 7 Days</option>
                            <option value="14">Past 14 Days</option>
                            <option value="30">Past 30 Days</option>
                        </select>
                    </div>
                    <div class="search-input-box">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        <input type="text" id="searchInput" placeholder="Filter title or company...">
                    </div>
                </div>
            </div>

            <div class="tags-filter-row">
                <span class="tags-title">Skills:</span>
                <div class="chips-list">
                    <button class="chip-item active" data-kw="all">All Skills</button>
                    <button class="chip-item" data-kw="aso">ASO</button>
                    <button class="chip-item" data-kw="user acquisition">User Acquisition</button>
                    <button class="chip-item" data-kw="app growth">App Growth</button>
                    <button class="chip-item" data-kw="play store">Play Console</button>
                    <button class="chip-item" data-kw="monetization">AdMob & Monetization</button>
                </div>
            </div>

            <section class="results-container">
                <div class="results-header">
                    <h3 id="resultsSummaryTitle">Matching Job Opportunities</h3>
                    <span class="status-meta">Last updated: {date_str}</span>
                </div>
                <div id="jobsGrid" class="cards-grid"></div>
            </section>
        </main>

        <footer class="app-footer">
            <p>Automated Cloudflare Deployment • Updated via GitHub Actions</p>
        </footer>
    </div>

    <script>
        const allJobs = {jobs_json_embedded};
        let activeTab = "all";
        let activeKw = "all";
        let selectedDays = "all";
        let searchQuery = "";

        document.addEventListener("DOMContentLoaded", () => {{
            const dateFilter = document.getElementById("dateFilter");
            const searchInput = document.getElementById("searchInput");

            document.querySelectorAll(".tab-item").forEach(btn => {{
                btn.addEventListener("click", () => {{
                    document.querySelectorAll(".tab-item").forEach(b => b.classList.remove("active"));
                    btn.classList.add("active");
                    activeTab = btn.getAttribute("data-tab");
                    render();
                }});
            }});

            dateFilter.addEventListener("change", (e) => {{ selectedDays = e.target.value; render(); }});
            document.querySelectorAll(".chip-item").forEach(c => {{
                c.addEventListener("click", () => {{
                    document.querySelectorAll(".chip-item").forEach(i => i.classList.remove("active"));
                    c.classList.add("active");
                    activeKw = c.getAttribute("data-kw");
                    render();
                }});
            }});

            searchInput.addEventListener("input", (e) => {{ searchQuery = e.target.value.toLowerCase().trim(); render(); }});
            render();
        }});

        function isLocal(j) {{
            const s = (j.source || "").toLowerCase();
            const l = (j.location || "").toLowerCase();
            const t = (j.title || "").toLowerCase();
            return s.includes("islamabad") || s.includes("pakistan") || l.includes("islamabad") || l.includes("rawalpindi") || l.includes("pakistan") || t.includes("islamabad");
        }}

        function isWithinDays(addedAtStr, maxDays) {{
            if (!addedAtStr || maxDays === "all") return true;
            const diffDays = Math.abs(new Date() - new Date(addedAtStr)) / (1000 * 60 * 60 * 24);
            return diffDays <= parseFloat(maxDays);
        }}

        function render() {{
            let filtered = allJobs;
            if (activeTab === "local") filtered = filtered.filter(j => isLocal(j));
            else if (activeTab === "remote") filtered = filtered.filter(j => !isLocal(j));

            if (selectedDays !== "all") filtered = filtered.filter(j => isWithinDays(j.added_at, selectedDays));
            if (activeKw !== "all") {{
                filtered = filtered.filter(j => {{
                    const t = (j.title || "").toLowerCase();
                    const m = (j.matched_keywords || []).map(k => k.toLowerCase()).join(" ");
                    return t.includes(activeKw) || m.includes(activeKw);
                }});
            }}

            if (searchQuery) {{
                filtered = filtered.filter(j => {{
                    return (j.title||"").toLowerCase().includes(searchQuery) || (j.company||"").toLowerCase().includes(searchQuery);
                }});
            }}

            document.getElementById("resultsSummaryTitle").textContent = `${{filtered.length}} Job Opportunities Available`;

            const grid = document.getElementById("jobsGrid");
            if (filtered.length === 0) {{
                grid.innerHTML = '<div style="grid-column: 1/-1; padding:40px; text-align:center; color:#9ca3af;">No jobs match this filter.</div>';
                return;
            }}

            grid.innerHTML = filtered.map(j => {{
                const title = j.title || "Job Title";
                const link = j.url || j.link || "#";
                const company = j.company || "Employer";
                const location = j.location || (isLocal(j) ? "Islamabad / Rawalpindi" : "Remote");
                const source = j.source || "LinkedIn";
                const skills = (j.matched_keywords || []).map(k => `<span class="skill-badge">${{k}}</span>`).join("");
                const date = j.added_at ? new Date(j.added_at).toLocaleDateString(undefined, {{month:'short', day:'numeric', year:'numeric'}}) : 'Fresh';

                return `
                    <div class="job-card">
                        <div>
                            <span class="source-tag">${{source}}</span>
                            <h4 class="job-title"><a href="${{link}}" target="_blank">${{title}}</a></h4>
                            <div class="meta-row"><span>🏢 ${{company}}</span></div>
                            <div class="meta-row"><span>📍 ${{location}}</span></div>
                            <div class="skills-list">${{skills}}</div>
                        </div>
                        <div class="card-footer">
                            <span class="date-text">${{date}}</span>
                            <a href="${{link}}" target="_blank" class="btn-apply">Apply Now ➔</a>
                        </div>
                    </div>
                `;
            }}).join("");
        }}
    </script>
</body>
</html>"""

    with open(dist_html_path, "w", encoding="utf-8") as f:
        f.write(dist_html_content)

    print(f"[Reports] Generated static Cloudflare Pages site: file:///{dist_html_path.as_posix()}")
    return str(html_path), str(dist_html_path)
