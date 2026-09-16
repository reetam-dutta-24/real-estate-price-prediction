import os
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIGURES_DIR = os.path.join(PROJECT_ROOT, "reports", "figures")


def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    h1, h2, h3 {
        font-family: 'Fraunces', serif;
        color: #16231D;
        letter-spacing: -0.01em;
    }
    

    .section-card {
        background: #FFFFFF;
        border: 1px solid #D9DED4;
        border-top: 3px solid #A9782F;
        padding: 1.5rem 1.7rem;
        margin-bottom: 1.2rem;
    }
    .section-card.teal { border-top-color: #2F6E68; }

    .badge {
        display: inline-block;
        background: #EEF2ED;
        border: 1px solid #D9DED4;
        color: #47564D;
        padding: 0.2rem 0.65rem;
        font-size: 0.78rem;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    /* ---------- WELCOME BOX ---------- */
    .welcome-box {
        background: #F4EFE3;
        border-left: 3px solid #A9782F;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.6rem;
    }
    .welcome-title {
        font-family: 'Fraunces', serif;
        font-size: 1.15rem;
        color: #16231D;
        margin-bottom: 0.3rem;
    }
    .welcome-msg { font-size: 0.9rem; color: #47564D; line-height: 1.5; }

    /* ---------- KPI CARDS ---------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin: 0 0 1.6rem 0;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #D9DED4;
        border-top: 3px solid var(--kpi-accent, #A9782F);
        padding: 1.2rem 1.3rem;
    }
    .kpi-number {
        font-family: 'Fraunces', serif;
        font-size: 1.9rem;
        font-weight: 600;
        color: #16231D;
        line-height: 1;
    }
    .kpi-label { font-size: 0.82rem; color: #47564D; margin-top: 0.4rem; font-weight: 500; }
    .kpi-desc { font-size: 0.75rem; color: #7C8C80; margin-top: 0.25rem; }

    /* ---------- SKELETON LOADING ---------- */
    .skeleton {
        background: linear-gradient(90deg, #E3E8E0 25%, #EEF2ED 37%, #E3E8E0 63%);
        background-size: 400% 100%;
        animation: skeleton-shimmer 1.4s ease infinite;
    }
    @keyframes skeleton-shimmer {
        0% { background-position: 100% 50%; }
        100% { background-position: 0 50%; }
    }
    .skeleton-line { height: 14px; margin-bottom: 0.55rem; }
    .skeleton-line:last-child { width: 60%; }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background-color: #16231D;
        border-right: 1px solid #23342C;
    }

    .sb-logo {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.3rem 0 1.1rem 0;
        border-bottom: 1px solid #2A3A32;
        margin-bottom: 0.4rem;
    }
    .sb-logo-mark {
        width: 34px; height: 34px;
        background: #A9782F;
        color: #16231D;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 0.92rem;
    }
    .sb-logo-title { font-family: 'Fraunces', serif; font-size: 1rem; color: #F5F7F4; font-weight: 600; line-height: 1.1; }
    .sb-logo-sub { font-size: 0.68rem; color: #8FA093; letter-spacing: 0.03em; margin-top: 0.1rem; }

    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
        color: #E9EDE7 !important;
        font-size: 0.92rem;
        border-radius: 0;
        padding: 0.55rem 0.9rem;
    }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {
        background-color: #1E2E27 !important;
        color: #F5F7F4 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background-color: #23342C !important;
        color: #E8C77E !important;
        border-left: 2px solid #A9782F;
    }

    .sb-label {
        font-size: 0.7rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #7C8C80;
        margin: 1.3rem 0 0.6rem 0;
        font-weight: 600;
    }
    .sb-howto-item {
        display: flex;
        gap: 0.55rem;
        font-size: 0.82rem;
        color: #D7DED3;
        padding: 0.35rem 0;
        align-items: flex-start;
        line-height: 1.4;
    }
    .sb-howto-num {
        flex-shrink: 0;
        width: 18px; height: 18px;
        border: 1px solid #3A4B41;
        color: #A9B7AC;
        font-size: 0.7rem;
        display: flex; align-items: center; justify-content: center;
        margin-top: 0.05rem;
    }
        /* Hide Streamlit's default page nav — we build our own below */
    [data-testid="stSidebarNav"] { display: none; }

    /* Fallback: catch any sidebar text our custom classes don't already color */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] label {
        color: #E9EDE7;
    }

    .sb-nav-link {
        display: block;
        padding: 0.5rem 0.7rem;
        margin-bottom: 0.15rem;
        color: #E9EDE7 !important;
        text-decoration: none !important;
        font-size: 0.92rem;
        border-left: 2px solid transparent;
    }
    .sb-nav-link:hover {
        background-color: #1E2E27;
        color: #F5F7F4 !important;
    }

    @media (max-width: 640px) {
        .section-card { padding: 1.1rem 1.2rem; }
        .kpi-number { font-size: 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_logo():
    st.sidebar.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-mark">KC</div>
        <div>
            <div class="sb-logo-title">Home Value</div>
            <div class="sb-logo-sub">King County, WA</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_howto():
    st.sidebar.markdown('<div class="sb-label">How to use</div>', unsafe_allow_html=True)
    steps = [
        "Browse market trends in Market Explorer.",
        "Enter property details in Predict.",
        "Review model performance in Model Insights.",
    ]
    html = ""
    for i, step in enumerate(steps, start=1):
        html += f'<div class="sb-howto-item"><span class="sb-howto-num">{i}</span><span>{step}</span></div>'
    st.sidebar.markdown(html, unsafe_allow_html=True)


def render_sidebar():
    sidebar_logo()

    st.sidebar.markdown('<div class="sb-label">Navigate</div>', unsafe_allow_html=True)
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Predict.py", label="Predict")
    st.sidebar.page_link("pages/2_Market_Explorer.py", label="Market Explorer")
    st.sidebar.page_link("pages/3_Model_Insights.py", label="Model Insights")
    st.sidebar.page_link("pages/4_About.py", label="About")

    sidebar_howto()

def welcome_box(title, message):
    st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-title">{title}</div>
        <div class="welcome-msg">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def kpi_cards(cards):
    """cards: list of dicts with keys: number, label, desc (optional), accent ('brass'|'teal')"""
    html = '<div class="kpi-grid">'
    for c in cards:
        accent = "#2F6E68" if c.get("accent") == "teal" else "#A9782F"
        desc_html = f'<div class="kpi-desc">{c["desc"]}</div>' if c.get("desc") else ""
        html += f"""<div class="kpi-card" style="--kpi-accent:{accent}">
            <div class="kpi-number">{c['number']}</div>
            <div class="kpi-label">{c['label']}</div>
            {desc_html}
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def skeleton_lines(n=3):
    html = "".join(['<div class="skeleton skeleton-line"></div>' for _ in range(n)])
    st.markdown(html, unsafe_allow_html=True)


def section_card_open(accent="brass"):
    cls = "section-card teal" if accent == "teal" else "section-card"
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)


def section_card_close():
    st.markdown('</div>', unsafe_allow_html=True)