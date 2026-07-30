document.addEventListener("DOMContentLoaded", () => {
    let allJobs = [];
    let activeTab = "all";
    let activeKw = "all";
    let selectedDays = "all";
    let searchQuery = "";

    // DOM Elements
    const findJobsBtn = document.getElementById("findJobsBtn");
    const btnSpinner = document.getElementById("btnSpinner");
    const jobsGrid = document.getElementById("jobsGrid");
    const loadingOverlay = document.getElementById("loadingOverlay");
    const searchInput = document.getElementById("searchInput");
    const dateFilter = document.getElementById("dateFilter");
    const lastUpdated = document.getElementById("lastUpdated");
    const resultsSummaryTitle = document.getElementById("resultsSummaryTitle");

    // SVG Icons
    const companySvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 4-4H8a4 4 0 0 4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;
    const locationSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>`;
    const externalLinkSvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`;
    const refreshSvg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>`;

    // Load initial jobs
    loadSavedJobs();

    // Event Listener: Search Button
    if (findJobsBtn) {
        findJobsBtn.addEventListener("click", () => {
            triggerLiveScrape();
        });
    }

    // Event Listener: Tabs
    document.querySelectorAll(".tab-item").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-item").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeTab = btn.getAttribute("data-tab");
            renderJobs();
        });
    });

    // Event Listener: Date Filter
    if (dateFilter) {
        dateFilter.addEventListener("change", (e) => {
            selectedDays = e.target.value;
            renderJobs();
        });
    }

    // Event Listener: Skill Chips
    document.querySelectorAll(".chip-item").forEach(chip => {
        chip.addEventListener("click", () => {
            document.querySelectorAll(".chip-item").forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            activeKw = chip.getAttribute("data-kw");
            renderJobs();
        });
    });

    // Event Listener: Search Input
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderJobs();
        });
    }

    // Fetch Saved Jobs API
    async function loadSavedJobs() {
        try {
            const res = await fetch("/api/jobs");
            const data = await res.json();
            if (data.success) {
                allJobs = data.jobs || [];
                renderJobs();
            }
        } catch (err) {
            console.error("Error loading saved jobs:", err);
        }
    }

    // Trigger Live Scrape API
    async function triggerLiveScrape() {
        if (findJobsBtn) findJobsBtn.disabled = true;
        if (btnSpinner) btnSpinner.style.display = "inline-block";
        if (loadingOverlay) loadingOverlay.classList.remove("hidden");

        try {
            const res = await fetch("/api/scrape", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ dry_run: false, timeframe_days: selectedDays })
            });

            const data = await res.json();

            if (data.success) {
                allJobs = data.jobs || [];
                if (lastUpdated) lastUpdated.textContent = "Updated " + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            } else {
                alert("Scraping finished: " + (data.error || "Done"));
            }
        } catch (err) {
            console.error("Scrape error:", err);
            alert("Connection error. Ensure app.py is running on http://localhost:5000.");
        } finally {
            if (findJobsBtn) findJobsBtn.disabled = false;
            if (btnSpinner) btnSpinner.style.display = "none";
            if (loadingOverlay) loadingOverlay.classList.add("hidden");
            renderJobs();
        }
    }

    // Helper: Formatter for Job Posting Date
    function formatPostingDate(job) {
        const raw = job.pub_date || job.added_at;
        if (!raw) return 'Recently Posted';

        const str = String(raw).trim();
        const lower = str.toLowerCase();

        // Platform relative strings (e.g. "2 days ago", "3 weeks ago", "1 day ago", "Just posted")
        if (lower.includes('ago') || lower.includes('just') || lower.includes('yesterday') || lower.includes('today')) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }

        // Standard date string parsing (e.g. "2026-07-28" or ISO string)
        const parsed = new Date(str);
        if (!isNaN(parsed.getTime())) {
            const now = new Date();
            const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const jobDate = new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate());
            const diffMs = today - jobDate;
            const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

            if (diffDays <= 0) return 'Posted Today';
            if (diffDays === 1) return 'Posted 1 day ago';
            if (diffDays <= 30) return `Posted ${diffDays} days ago`;

            return 'Posted ' + parsed.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
        return str;
    }

    // Helper: Date Range Filter
    function isWithinDays(job, maxDays) {
        if (maxDays === "all") return true;
        const raw = job.pub_date || job.added_at;
        if (!raw) return true;

        const lower = String(raw).toLowerCase();

        if (lower.includes('ago')) {
            if (lower.includes('hour') || lower.includes('minute') || lower.includes('just')) {
                return true;
            }
            if (lower.includes('week')) {
                const match = lower.match(/(\d+)/);
                const weeks = match ? parseInt(match[1], 10) : 1;
                return (weeks * 7) <= parseFloat(maxDays);
            }
            if (lower.includes('day')) {
                const match = lower.match(/(\d+)/);
                const days = match ? parseInt(match[1], 10) : 1;
                return days <= parseFloat(maxDays);
            }
            if (lower.includes('month')) {
                const match = lower.match(/(\d+)/);
                const months = match ? parseInt(match[1], 10) : 1;
                return (months * 30) <= parseFloat(maxDays);
            }
        }

        const parsed = new Date(raw);
        if (!isNaN(parsed.getTime())) {
            const now = new Date();
            const diffMs = Math.abs(now - parsed);
            const diffDays = diffMs / (1000 * 60 * 60 * 24);
            return diffDays <= (parseFloat(maxDays) + 0.5);
        }
        return true;
    }

    // Helper: Is Local Job
    function isLocalJob(job) {
        const src = (job.source || "").toLowerCase();
        const loc = (job.location || "").toLowerCase();
        const title = (job.title || "").toLowerCase();
        return src.includes("islamabad") || src.includes("pakistan") || loc.includes("islamabad") || loc.includes("rawalpindi") || loc.includes("pakistan") || title.includes("islamabad");
    }

    // Render Filtered Jobs Grid
    function renderJobs() {
        let filtered = allJobs;

        // 1. Location Tab Filter
        if (activeTab === "local") {
            filtered = filtered.filter(j => isLocalJob(j));
        } else if (activeTab === "remote") {
            filtered = filtered.filter(j => !isLocalJob(j));
        }

        // 2. Timeframe Filter
        if (selectedDays !== "all") {
            filtered = filtered.filter(j => isWithinDays(j, selectedDays));
        }

        // 3. Skill Filter
        if (activeKw !== "all") {
            filtered = filtered.filter(j => {
                const title = (j.title || "").toLowerCase();
                const matched = (j.matched_keywords || []).map(k => k.toLowerCase()).join(" ");
                return title.includes(activeKw) || matched.includes(activeKw);
            });
        }

        // 4. Search Bar Query
        if (searchQuery) {
            filtered = filtered.filter(j => {
                const title = (j.title || "").toLowerCase();
                const comp = (j.company || "").toLowerCase();
                const src = (j.source || "").toLowerCase();
                return title.includes(searchQuery) || comp.includes(searchQuery) || src.includes(searchQuery);
            });
        }

        if (resultsSummaryTitle) {
            resultsSummaryTitle.textContent = `${filtered.length} Job Opportunities Found`;
        }

        if (filtered.length === 0) {
            jobsGrid.innerHTML = `
                <div class="empty-state-box">
                    <h4>No Job Listings Found for this Filter</h4>
                    <p>Try selecting another location tab or timeframe, or click below to search live platforms.</p>
                    <button class="btn-search" id="emptyStateFetchBtn" style="margin-top: 8px;">
                        ${refreshSvg}
                        <span>Fetch Latest Jobs from Platforms</span>
                    </button>
                </div>
            `;

            const emptyBtn = document.getElementById("emptyStateFetchBtn");
            if (emptyBtn) {
                emptyBtn.addEventListener("click", triggerLiveScrape);
            }
            return;
        }

        jobsGrid.innerHTML = filtered.map(job => {
            const title = job.title || "Untitled Position";
            const link = job.url || job.link || "#";
            const source = job.source || "Job Portal";
            const company = job.company || "Direct Employer";
            const location = job.location || (isLocalJob(job) ? "Islamabad / Rawalpindi, Pakistan" : "Remote Position");

            const skillsHtml = (job.matched_keywords || []).map(kw => `
                <span class="skill-badge">${kw}</span>
            `).join("");

            const dateStr = formatPostingDate(job);

            return `
                <div class="job-card">
                    <div class="card-main">
                        <span class="source-tag">${source}</span>
                        <h4 class="job-title">
                            <a href="${link}" target="_blank" rel="noopener">${title}</a>
                        </h4>
                        <div class="meta-row">${companySvg} <span>${company}</span></div>
                        <div class="meta-row">${locationSvg} <span>${location}</span></div>
                        ${skillsHtml ? `<div class="skills-list">${skillsHtml}</div>` : ''}
                    </div>
                    <div class="card-footer">
                        <span class="date-text">${dateStr}</span>
                        <a href="${link}" target="_blank" rel="noopener" class="btn-apply">
                            <span>Apply Now</span>
                            ${externalLinkSvg}
                        </a>
                    </div>
                </div>
            `;
        }).join("");
    }
});
