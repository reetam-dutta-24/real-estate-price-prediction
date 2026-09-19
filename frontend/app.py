import streamlit as st
from theme import inject_theme, render_sidebar, welcome_box, stat_strip, card, how_it_works_section

st.set_page_config(page_title="King County Home Value", layout="wide")
inject_theme()
render_sidebar()

st.title("King County Home Value")

welcome_box(
    "Welcome",
    "This tool estimates residential property values across King County, Washington, "
    "using a tuned XGBoost model trained on 21,613 real sales records (test R² = 0.91). "
    "Get a live estimate, explore the market, or see how the model performs."
)

stat_strip([
    ("21,613", "Sales records"),
    ("0.91", "Model R²"),
    ("$62K", "Typical error margin"),
    ("45", "Model features"),
])

st.markdown("### How it works")
how_it_works_section()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with card("predict-nav", accent="brass"):
        st.markdown("#### Predict")
        st.write("Walk through a short guided form and get a live estimate with a full report.")
        st.page_link("pages/1_Predict.py", label="Go to Predictor")
with col2:
    with card("market-nav", accent="teal"):
        st.markdown("#### Explore the Market")
        st.write("Price distributions, geographic patterns, and the analysis behind the model.")
        st.page_link("pages/2_Market_Explorer.py", label="Explore the Data")

col3, col4 = st.columns(2)
with col3:
    with card("insights-nav", accent="moss"):
        st.markdown("#### Model Insights")
        st.write("How the model was built, tuned, and how it performs.")
        st.page_link("pages/3_Model_Insights.py", label="View Insights")
with col4:
    with card("about-nav", accent="clay"):
        st.markdown("#### About This Project")
        st.write("The data, the pipeline, and the reasoning behind the build.")
        st.page_link("pages/4_About.py", label="Read More")