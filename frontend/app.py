import streamlit as st
from theme import inject_theme, render_sidebar, welcome_box, kpi_cards, section_card_open, section_card_close

st.set_page_config(page_title="King County Home Value", layout="wide")
inject_theme()
render_sidebar()

st.title("King County Home Value")

welcome_box(
    "Welcome",
    "This tool estimates residential property values across King County, Washington, "
    "using a model trained on 21,613 real sales records. Use the sidebar to get a prediction, "
    "explore the market, or see how the model performs."
)

kpi_cards([
    {"number": "21,613", "label": "Sales records", "desc": "King County, 2014–15"},
    {"number": "45", "label": "Model features", "desc": "After leakage-safe preprocessing", "accent": "teal"},
    {"number": "15", "label": "Geographic clusters", "desc": "Found via KMeans"},
    {"number": "3", "label": "Amenity components", "desc": "PCA-compressed from 50 landmarks", "accent": "teal"},
])

col1, col2 = st.columns(2)

with col1:
    section_card_open()
    st.markdown("#### Predict")
    st.write("Enter a property's details and get an estimated market value.")
    st.page_link("pages/1_Predict.py", label="Go to Predictor")
    section_card_close()

with col2:
    section_card_open(accent="teal")
    st.markdown("#### Explore the Market")
    st.write("Price distributions, geographic patterns, and the analysis behind the model.")
    st.page_link("pages/2_Market_Explorer.py", label="Explore the Data")
    section_card_close()

col3, col4 = st.columns(2)

with col3:
    section_card_open()
    st.markdown("#### Model Insights")
    st.write("How the model was built and how it performs.")
    st.page_link("pages/3_Model_Insights.py", label="View Insights")
    section_card_close()

with col4:
    section_card_open(accent="teal")
    st.markdown("#### About This Project")
    st.write("The data, the pipeline, and the reasoning behind the build.")
    st.page_link("pages/4_About.py", label="Read More")
    section_card_close()