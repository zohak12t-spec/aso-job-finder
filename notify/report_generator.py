import json
from datetime import datetime
from pathlib import Path
from config import BASE_DIR

DIST_DIR = BASE_DIR / "dist"
REPORTS_DIR = BASE_DIR / "reports"

def generate_reports(jobs: list) -> tuple:
    """
    Generates local jobs_report.html/md and standalone dist/index.html 
    with custom SVG favicon app icon and custom color scheme (#f5f3f0 canvas, #fefefe cards, #1a1816 primary buttons).
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ASO & App Growth Jobs</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="apple-touch-icon" href="favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #f5f3f0;
            --bg-surface: #fefefe;
            --bg-card: #fefefe;
            --bg-card-hover: #ffffff;
            --border-subtle: rgba(26, 24, 22, 0.07);
            --border-hover: rgba(26, 24, 22, 0.15);
            --text-primary: #1a1816;
            --text-secondary: #66625d;
            --text-tertiary: #8c8780;
            --brand-dark: #1a1816;
            --brand-dark-hover: #2e2b28;
            --font-family: 'Inter', 'Plus Jakarta Sans', sans-serif;
            --radius-md: 10px;
            --radius-lg: 14px;
            --shadow-smooth: 0 4px 20px rgba(26, 24, 22, 0.03);
            --shadow-hover: 0 8px 30px rgba(26, 24, 22, 0.07);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; text-transform: none !important; }}
        body {{ background-color: var(--bg-main); color: var(--text-primary); font-family: var(--font-family); min-height: 100vh; line-height: 1.5; -webkit-font-smoothing: antialiased; }}
        .app-layout {{ display: flex; flex-direction: column; min-height: 100vh; }}
        .app-header {{ background-color: var(--bg-surface); border-bottom: 1px solid var(--border-subtle); padding: 18px 0; }}
        .header-container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }}
        .brand {{ display: flex; align-items: center; gap: 12px; }}
        .brand-logo {{ width: 40px; height: 40px; background-color: var(--bg-main); color: var(--brand-dark); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        .brand-text h2 {{ font-size: 19px; font-weight: 600; color: var(--text-primary); }}
        .brand-text p {{ font-size: 13px; color: var(--text-secondary); }}
        .btn-search {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; background-color: var(--brand-dark); color: #fefefe; border: none; font-family: var(--font-family); font-size: 14px; font-weight: 600; padding: 10px 20px; border-radius: var(--radius-md); cursor: pointer; white-space: nowrap; text-decoration: none; box-shadow: 0 2px 8px rgba(26, 24, 22, 0.12); }}
        .btn-search:hover {{ background-color: var(--brand-dark-hover); }}
        .main-content {{ max-width: 1200px; width: 100%; margin: 0 auto; padding: 28px 20px 60px 20px; flex: 1; }}
        .toolbar-panel {{ background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 12px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; margin-bottom: 20px; box-shadow: var(--shadow-smooth); }}
        .toolbar-left, .toolbar-right {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
        .tab-group {{ display: flex; background-color: var(--bg-main); padding: 4px; border-radius: var(--radius-md); max-width: 100%; overflow-x: auto; }}
        .tab-item {{ background: transparent; border: none; color: var(--text-secondary); font-family: var(--font-family); font-size: 13px; font-weight: 500; padding: 7px 14px; border-radius: 6px; cursor: pointer; white-space: nowrap; }}
        .tab-item.active {{ background-color: var(--brand-dark); color: #fefefe; font-weight: 600; }}
        .select-input {{ background-color: var(--bg-main); border: 1px solid var(--border-subtle); color: var(--text-primary); font-family: var(--font-family); font-size: 13px; padding: 8px 12px; border-radius: var(--radius-md); outline: none; cursor: pointer; }}
        .search-input-box {{ display: flex; align-items: center; gap: 8px; background-color: var(--bg-main); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 8px 14px; width: 240px; color: var(--text-tertiary); }}
        .search-input-box input {{ background: transparent; border: none; outline: none; color: var(--text-primary); font-family: var(--font-family); font-size: 13px; width: 100%; }}
        .tags-filter-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 24px; flex-wrap: wrap; }}
        .chip-item {{ background-color: var(--bg-surface); border: 1px solid var(--border-subtle); color: var(--text-secondary); font-family: var(--font-family); font-size: 12px; padding: 5px 12px; border-radius: 20px; cursor: pointer; }}
        .chip-item.active {{ background-color: var(--brand-dark); border-color: var(--brand-dark); color: #fefefe; font-weight: 600; }}
        .results-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 8px; }}
        .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; }}
        .empty-state-box {{ grid-column: 1 / -1; background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 48px 24px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; box-shadow: var(--shadow-smooth); }}
        .empty-state-box h4 {{ font-size: 17px; font-weight: 600; color: var(--text-primary); }}
        .empty-state-box p {{ font-size: 13px; color: var(--text-secondary); max-width: 460px; }}
        .job-card {{ background-color: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 22px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-smooth); transition: all 0.15s ease; }}
        .job-card:hover {{ background-color: var(--bg-card-hover); border-color: var(--border-hover); box-shadow: var(--shadow-hover); transform: translateY(-2px); }}
        .source-tag {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; background-color: var(--bg-main); color: var(--text-secondary); margin-bottom: 12px; }}
        .job-title {{ font-size: 17px; font-weight: 600; line-height: 1.35; margin-bottom: 10px; }}
        .job-title a {{ color: var(--text-primary); text-decoration: none; }}
        .meta-row {{ display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }}
        .skills-list {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }}
        .skill-badge {{ background-color: var(--bg-main); color: var(--text-secondary); font-size: 11px; padding: 3px 9px; border-radius: 4px; font-weight: 500; }}
        .card-footer {{ padding-top: 16px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; }}
        .date-text {{ font-size: 12px; color: var(--text-tertiary); }}
        .btn-apply {{ display: inline-flex; align-items: center; gap: 6px; background-color: var(--brand-dark); color: #fefefe; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600; }}
        .btn-apply:hover {{ opacity: 0.9; }}
        .app-footer {{ text-align: center; padding: 24px; font-size: 13px; color: var(--text-tertiary); border-top: 1px solid var(--border-subtle); }}
        @media (max-width: 768px) {{
            .header-container {{ flex-direction: column; align-items: stretch; }}
            .btn-search {{ width: 100%; padding: 12px 18px; font-size: 15px; }}
            .toolbar-panel {{ flex-direction: column; align-items: stretch; }}
            .toolbar-left, .toolbar-right {{ width: 100%; }}
            .tab-group {{ width: 100%; justify-content: space-around; }}
            .search-input-box {{ width: 100%; }}
            .cards-grid {{ grid-template-columns: 1fr; }}
            .main-content {{ padding: 18px 14px 40px 14px; }}
        }}
    </style>
</head>
<body>
    <div class="app-layout">
        <header class="app-header">
            <div class="header-container">
                <div class="brand">
                    <div class="brand-logo">
                        <svg width="24" height="24" viewBox="0 0 64 64" fill="none">
                            <rect width="64" height="64" rx="16" fill="#1a1816"/>
                            <path d="M24 22V18A4 4 0 0 1 28 14H36A4 4 0 0 1 40 18V22" stroke="#fefefe" stroke-width="4" stroke-linecap="round"/>
                            <rect x="14" y="22" width="36" height="26" rx="5" fill="#fefefe"/>
                            <path d="M22 38L30 30L34 34L42 26" stroke="#1a1816" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <polyline points="36 26 42 26 42 32" stroke="#1a1816" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div class="brand-text">
                        <h2>ASO & App Growth Jobs</h2>
                        <p>Curated roles for Islamabad, Rawalpindi, and Remote</p>
                    </div>
                </div>

                <div class="action-wrapper">
                    <button class="btn-search" onclick="location.reload()">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
                        <span>Fetch Latest Jobs from Platforms</span>
                    </button>
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
                grid.innerHTML = `
                    <div class="empty-state-box">
                        <h4>No Job Listings Found for this Filter</h4>
                        <p>Try changing your location tab or timeframe, or click below to refresh live listings.</p>
                        <button class="btn-search" onclick="location.reload()" style="margin-top: 8px;">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
                            <span>Fetch Latest Jobs from Platforms</span>
                        </button>
                    </div>
                `;
                return;
            }}

            grid.innerHTML = filtered.map(j => {{
                const title = j.title || "Job Title";
                const link = j.url || j.link || "#";
                const company = j.company || "Employer";
                const location = j.location || (isLocal(j) ? "Islamabad / Rawalpindi, Pakistan" : "Remote Position");
                const source = j.source || "LinkedIn";
                const skills = (j.matched_keywords || []).map(k => `<span class="skill-badge">${{k}}</span>`).join("");
                const date = j.added_at ? new Date(j.added_at).toLocaleDateString(undefined, {{month:'short', day:'numeric', year:'numeric'}}) : 'Fresh';

                return `
                    <div class="job-card">
                        <div class="card-main">
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
