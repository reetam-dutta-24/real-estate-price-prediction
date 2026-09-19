import os
import streamlit as st
import pydeck as pdk
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIGURES_DIR = os.path.join(PROJECT_ROOT, "reports", "figures")


def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Fraunces', serif; color: #16231D; letter-spacing: -0.01em; }

    header[data-testid="stHeader"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stAppViewBlockContainer"] { animation: fadeSlideIn 0.35s ease; }

    /* ---------- STAT STRIP ---------- */
    .stat-strip {
        display: flex; flex-wrap: wrap;
        border-top: 1px solid #D9DED4; border-bottom: 1px solid #D9DED4;
        margin: 1.4rem 0 2rem 0;
    }
    .stat-block { flex: 1 1 140px; min-width: 140px; padding: 1.1rem 1.4rem; border-right: 1px solid #D9DED4; }
    .stat-block:last-child { border-right: none; }
    .stat-number { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 600; color: #16231D; line-height: 1; }
    .stat-label { font-size: 0.8rem; color: #47564D; margin-top: 0.35rem; }

        /* ---------- REAL BORDERED CARDS — now with depth ---------- */
    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #EEF2ED 0%, #E7ECE3 100%) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 0 !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius: 12px !important;
        border: 1px solid #E3E8E0 !important;
        box-shadow: 0 1px 2px rgba(22,35,29,0.05), 0 10px 28px rgba(22,35,29,0.07);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
        padding-top: 0.4rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        box-shadow: 0 2px 4px rgba(22,35,29,0.06), 0 16px 36px rgba(22,35,29,0.10);
        transform: translateY(-2px);
    }

    div[class*="st-key-brass_"] > div {
        background: linear-gradient(160deg, #FFFDF7 0%, #FFFFFF 55%);
        border-top: 4px solid #A9782F !important;
        box-shadow: 0 1px 2px rgba(169,120,47,0.10), 0 10px 28px rgba(169,120,47,0.12) !important;
    }
    div[class*="st-key-teal_"] > div {
        background: linear-gradient(160deg, #F6FAF9 0%, #FFFFFF 55%);
        border-top: 4px solid #2F6E68 !important;
        box-shadow: 0 1px 2px rgba(47,110,104,0.10), 0 10px 28px rgba(47,110,104,0.12) !important;
    }
    div[class*="st-key-moss_"] > div {
        background: linear-gradient(160deg, #F7FAF5 0%, #FFFFFF 55%);
        border-top: 4px solid #6B8F5E !important;
        box-shadow: 0 1px 2px rgba(107,143,94,0.10), 0 10px 28px rgba(107,143,94,0.12) !important;
    }
    div[class*="st-key-clay_"] > div {
        background: linear-gradient(160deg, #FDF6F1 0%, #FFFFFF 55%);
        border-top: 4px solid #B0562E !important;
        box-shadow: 0 1px 2px rgba(176,86,46,0.10), 0 10px 28px rgba(176,86,46,0.12) !important;
    }
    .badge {
        display: inline-block; background: #EEF2ED; border: 1px solid #D9DED4; color: #47564D;
        padding: 0.2rem 0.65rem; font-size: 0.78rem; margin-right: 0.4rem; margin-bottom: 0.4rem;
    }

    /* ---------- WELCOME BOX ---------- */
    .welcome-box { background: #F4EFE3; border-left: 3px solid #A9782F; padding: 1.1rem 1.4rem; margin-bottom: 1.6rem; }
    .welcome-title { font-family: 'Fraunces', serif; font-size: 1.15rem; color: #16231D; margin-bottom: 0.3rem; }
    .welcome-msg { font-size: 0.9rem; color: #47564D; line-height: 1.5; }

        .kpi-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FAFBF9 100%);
        border: 1px solid #E3E8E0; border-top: 3px solid var(--kpi-accent, #A9782F);
        border-radius: 10px; padding: 1.3rem 1.4rem;
        box-shadow: 0 1px 2px rgba(22,35,29,0.04), 0 8px 20px rgba(22,35,29,0.05);
    }
    /* ---------- SKELETON ---------- */
    .skeleton { background: linear-gradient(90deg, #E3E8E0 25%, #EEF2ED 37%, #E3E8E0 63%); background-size: 400% 100%; animation: skeleton-shimmer 1.4s ease infinite; }
    @keyframes skeleton-shimmer { 0% { background-position: 100% 50%; } 100% { background-position: 0 50%; } }
    .skeleton-line { height: 14px; margin-bottom: 0.55rem; }
    .skeleton-line:last-child { width: 60%; }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] { background-color: #16231D; border-right: 1px solid #23342C; }
    [data-testid="stSidebarNav"] { display: none; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] a, section[data-testid="stSidebar"] label { color: #E9EDE7; }

    .sb-logo { display: flex; align-items: center; gap: 0.65rem; padding: 0.3rem 0 1.1rem 0; border-bottom: 1px solid #2A3A32; margin-bottom: 0.4rem; }
    .sb-logo-mark { width: 34px; height: 34px; background: #A9782F; color: #16231D; display: flex; align-items: center; justify-content: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 0.92rem; }
    .sb-logo-title { font-family: 'Fraunces', serif; font-size: 1rem; color: #F5F7F4; font-weight: 600; line-height: 1.1; }
    .sb-logo-sub { font-size: 0.68rem; color: #8FA093; letter-spacing: 0.03em; margin-top: 0.1rem; }

    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] { color: #E9EDE7 !important; font-size: 0.92rem; border-radius: 0; padding: 0.55rem 0.9rem; }
    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover { background-color: #1E2E27 !important; color: #F5F7F4 !important; }
    section[data-testid="stSidebar"] a[aria-current="page"] { background-color: #23342C !important; color: #E8C77E !important; border-left: 2px solid #A9782F; }

    .sb-label { font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase; color: #7C8C80; margin: 1.3rem 0 0.6rem 0; font-weight: 600; }
    .sb-howto-item { display: flex; gap: 0.55rem; font-size: 0.82rem; color: #D7DED3; padding: 0.35rem 0; align-items: flex-start; line-height: 1.4; }
    .sb-howto-num { flex-shrink: 0; width: 18px; height: 18px; border: 1px solid #3A4B41; color: #A9B7AC; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; margin-top: 0.05rem; }

    /* ---------- FORM SECTIONS ---------- */
    .form-section-title { font-family: 'Fraunces', serif; font-size: 1.05rem; color: #16231D; margin: 0 0 0.2rem 0; }
    .form-section-sub { font-size: 0.82rem; color: #7C8C80; margin-bottom: 0.9rem; }
    .field-hint { font-size: 0.78rem; color: #7C8C80; margin-top: -0.6rem; margin-bottom: 0.6rem; }

        .spec-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FAFBF9 100%);
        border: 1px solid #E3E8E0; border-radius: 10px; padding: 1.4rem 1.5rem;
        box-shadow: 0 1px 2px rgba(22,35,29,0.04), 0 8px 20px rgba(22,35,29,0.05);
    }
        .valuation-card {
        background: radial-gradient(circle at 15% 15%, #FBF4E4 0%, #FFFFFF 45%);
        border: 1px solid #E9DCC0;
        border-radius: 14px;
        padding: 2.1rem 2.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(169,120,47,0.10), 0 14px 34px rgba(169,120,47,0.14);
        position: relative;
        overflow: hidden;
    }
    .valuation-card::before {
        content: "";
        position: absolute; top: -40px; right: -40px;
        width: 140px; height: 140px; border-radius: 50%;
        background: radial-gradient(circle, rgba(169,120,47,0.14), transparent 70%);
    }
    .valuation-label { font-size: 0.8rem; color: #8A6A30; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600; }
    .valuation-price {
        font-family: 'Fraunces', serif; font-size: 3.1rem; font-weight: 600;
        color: #16231D; line-height: 1.15; margin: 0.25rem 0 0.5rem 0;
        text-shadow: 0 1px 0 rgba(255,255,255,0.6);
    }
    .valuation-note { font-size: 0.87rem; color: #5A6B5E; }

    /* ---------- FACTOR BARS ---------- */
    .factor-row { margin-bottom: 0.7rem; }
    .factor-label { display: flex; justify-content: space-between; font-size: 0.85rem; color: #16231D; margin-bottom: 0.25rem; }
    .factor-track { background: #EEF2ED; height: 6px; width: 100%; position: relative; }
    .factor-fill { height: 6px; position: absolute; top: 0; }
    .factor-fill.up { background: #A9782F; left: 50%; }
    .factor-fill.down { background: #2F6E68; right: 50%; }
    .factor-center { position: absolute; left: 50%; top: -3px; width: 1px; height: 12px; background: #D9DED4; }

    /* ---------- STEPPER ---------- */
    .stepper { display: flex; align-items: center; margin: 0.5rem 0 2rem 0; }
    .stepper-item { display: flex; flex-direction: column; align-items: center; gap: 0.4rem; }
    .stepper-dot { width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.82rem; font-weight: 600; border: 2px solid #D9DED4; color: #7C8C80; background: #FFFFFF; }
    .stepper-item.active .stepper-dot { border-color: #A9782F; color: #A9782F; background: #FBF6EC; }
    .stepper-item.done .stepper-dot { border-color: #2F6E68; background: #2F6E68; color: #FFFFFF; }
    .stepper-label { font-size: 0.76rem; color: #7C8C80; white-space: nowrap; }
    .stepper-item.active .stepper-label { color: #16231D; font-weight: 600; }
    .stepper-line { flex: 1; height: 2px; background: #D9DED4; margin: 0 0.5rem 1.4rem 0.5rem; }

        .how-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #FAFBF9 100%);
        border: 1px solid #E3E8E0; border-radius: 10px; padding: 1.5rem 1.4rem; height: 100%;
        box-shadow: 0 1px 2px rgba(22,35,29,0.04), 0 8px 20px rgba(22,35,29,0.05);
    }
    /* ---------- LIST ROWS ---------- */
    .list-row { display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0; border-bottom: 1px solid #EEF2ED; }
    .list-row:last-child { border-bottom: none; }
    .list-row-main { font-size: 0.9rem; color: #16231D; font-weight: 500; }
    .list-row-sub { font-size: 0.76rem; color: #7C8C80; margin-top: 0.1rem; }
    .list-row-value { font-size: 0.88rem; color: #16231D; font-weight: 600; text-align: right; }
    .list-row-tag { font-size: 0.7rem; color: #47564D; background: #EEF2ED; border: 1px solid #D9DED4; padding: 0.1rem 0.5rem; margin-top: 0.15rem; display: inline-block; }

        .pct-track {
        background: linear-gradient(90deg, #EEF2ED, #D9DED4);
        height: 12px; width: 100%; position: relative; margin: 0.9rem 0 0.6rem 0;
        border-radius: 999px; overflow: visible;
    }
    .pct-marker {
        position: absolute; top: -6px; width: 4px; height: 24px;
        background: #A9782F; border-radius: 2px;
        box-shadow: 0 0 0 3px rgba(169,120,47,0.18);
    }
    .confidence-bar { background: #EEF2ED; height: 10px; width: 100%; position: relative; margin: 0.7rem 0; border-radius: 999px; overflow: hidden; }
    .confidence-fill {
        background: linear-gradient(90deg, #C99A54, #A9782F);
        height: 10px; position: absolute; left: 0; border-radius: 999px;
    }
    /* ---------- METRIC TABLE ---------- */
    .metric-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    .metric-table th { text-align: left; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; color: #7C8C80; padding: 0.5rem 0.7rem; border-bottom: 1px solid #D9DED4; }
    .metric-table td { padding: 0.6rem 0.7rem; border-bottom: 1px solid #EEF2ED; color: #16231D; }
    .metric-table tr.highlight td { background: #FBF6EC; font-weight: 600; }

    .print-btn { display: inline-block; background: #16231D; color: #EEF2ED !important; border: none; padding: 0.55rem 1.1rem; font-size: 0.85rem; cursor: pointer; text-decoration: none; }
    .print-btn:hover { background: #2A3A32; }

    @media (max-width: 640px) {
        .kpi-number { font-size: 1.5rem; }
        .valuation-price { font-size: 2.1rem; }
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


def render_sidebar():
    sidebar_logo()
    st.sidebar.markdown('<div class="sb-label">Navigate</div>', unsafe_allow_html=True)
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Predict.py", label="Predict")
    st.sidebar.page_link("pages/2_Market_Explorer.py", label="Market Explorer")
    st.sidebar.page_link("pages/3_Model_Insights.py", label="Model Insights")
    st.sidebar.page_link("pages/4_About.py", label="About")


def welcome_box(title, message):
    st.markdown(f"""
    <div class="welcome-box">
        <div class="welcome-title">{title}</div>
        <div class="welcome-msg">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_strip(stats):
    html = '<div class="stat-strip">'
    for number, label in stats:
        html += f'<div class="stat-block"><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def kpi_cards(cards):
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


def card(key, accent="brass"):
    """Real bordered container. Use as: with card('mykey', accent='teal'): ..."""
    return st.container(border=True, key=f"{accent}_{key}")


def step_indicator(current_step, steps):
    html = '<div class="stepper">'
    for i, label in enumerate(steps, start=1):
        state = "done" if i < current_step else ("active" if i == current_step else "")
        dot_content = "✓" if i < current_step else str(i)
        html += f'<div class="stepper-item {state}"><div class="stepper-dot">{dot_content}</div><div class="stepper-label">{label}</div></div>'
        if i != len(steps):
            html += '<div class="stepper-line"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def how_it_works_section():
    steps = [
        ("1", "Tell us about the home", "Walk through a short, guided form — size, condition, and location."),
        ("2", "We run it through the model", "A tuned XGBoost model, trained on 21,613 real King County sales, generates an estimate."),
        ("3", "Get a full report", "See the estimate, what's driving it, comparable sales, and nearby amenities."),
    ]
    cols = st.columns(3)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="how-card">
                <div class="how-num">{num}</div>
                <div class="how-title">{title}</div>
                <div class="how-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def spec_card(specs):
    html = '<div class="spec-card"><div class="spec-card-title">Property Snapshot</div>'
    for label, value in specs:
        html += f'<div class="spec-row"><span>{label}</span><span>{value}</span></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def factor_bars(factors):
    html = ""
    for f in factors:
        width = max(f['magnitude'] * 50, 4)
        arrow = "↑" if f['direction'] == 'up' else "↓"
        html += f"""
        <div class="factor-row">
            <div class="factor-label"><span>{f['label']}</span><span>{arrow}</span></div>
            <div class="factor-track">
                <div class="factor-center"></div>
                <div class="factor-fill {f['direction']}" style="width:{width}%"></div>
            </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def list_row(main, sub, value, tag=None):
    tag_html = f'<div class="list-row-tag">{tag}</div>' if tag else ""
    st.markdown(f"""
    <div class="list-row">
        <div><div class="list-row-main">{main}</div><div class="list-row-sub">{sub}</div>{tag_html}</div>
        <div class="list-row-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def percentile_meter(percentile, caption):
    st.markdown(f"""
    <div class="pct-track"><div class="pct-marker" style="left:{percentile}%"></div></div>
    <div class="pct-caption">{caption}</div>
    """, unsafe_allow_html=True)


def metric_table(rows, highlight_label=None):
    html = '<table class="metric-table"><tr><th>Model</th><th>Test RMSE (log)</th><th>Test MAE ($)</th><th>R²</th></tr>'
    for r in rows:
        cls = "highlight" if r["model"] == highlight_label else ""
        html += f'<tr class="{cls}"><td>{r["model"]}</td><td>{r["rmse"]}</td><td>{r["mae"]}</td><td>{r["r2"]}</td></tr>'
    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)


def pin_map(house_lat, house_long, points, height=280):
    house_df = pd.DataFrame({'lat': [house_lat], 'lon': [house_long]})
    point_df = pd.DataFrame([
        {"lat": p["lat"], "lon": p["long"], "label": p["name"], "sub": f"{p['category']} · {p['distance_km']:.1f} km"}
        for p in points
    ]) if points else pd.DataFrame(columns=["lat", "lon", "label", "sub"])

    view_state = pdk.ViewState(latitude=house_lat, longitude=house_long, zoom=10.5, pitch=0)
    house_layer = pdk.Layer("ScatterplotLayer", data=house_df, get_position='[lon, lat]',
                             get_color='[169, 120, 47, 230]', get_radius=280, pickable=True,
                             stroked=True, get_line_color='[22,35,29,255]', line_width_min_pixels=2)
    point_layer = pdk.Layer("ScatterplotLayer", data=point_df, get_position='[lon, lat]',
                             get_color='[47, 110, 104, 190]', get_radius=140, pickable=True)

    st.pydeck_chart(pdk.Deck(
        layers=[point_layer, house_layer],
        initial_view_state=view_state,
        map_style="road",
        tooltip={"text": "{label}\n{sub}"}
    ), height=height)