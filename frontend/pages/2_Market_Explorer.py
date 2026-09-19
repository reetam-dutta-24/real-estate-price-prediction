import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, stat_strip, FIGURES_DIR, card

st.set_page_config(page_title="Market Explorer", layout="wide")
inject_theme()
render_sidebar()

st.title("Market Explorer")
welcome_box("Explore the data", "Findings from exploratory analysis of 21,613 King County home sales — the same dataset and features behind the prediction model.")

stat_strip([
    ("$450K", "Median sale price"),
    ("$7.7M", "Highest recorded sale"),
    ("70", "Zipcodes covered"),
    ("15", "Geographic clusters"),
])


def show_figure(filename, caption):
    path = os.path.join(FIGURES_DIR, filename)
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"Figure not generated yet: {filename}")


col1, col2 = st.columns(2)
with col1:
    with card("price-dist", accent="brass"):
        st.markdown("#### Price Distribution")
        show_figure("price_distribution.png", "Right-skewed — most homes cluster $300K–$600K, with a long luxury tail.")
        st.caption("The model trains on log-transformed price to handle this skew properly.")
with col2:
    with card("geo-price", accent="teal"):
        st.markdown("#### Geography of Price")
        show_figure("geo_price_map.png", "Price by location — waterfront and central areas command a premium.")

col3, col4 = st.columns(2)
with col3:
    with card("correlation", accent="moss"):
        st.markdown("#### Feature Correlation")
        show_figure("correlation_heatmap.png", "sqft_living, grade, and bathrooms move together — addressed via VIF analysis.")
with col4:
    with card("clusters", accent="clay"):
        st.markdown("#### Geographic Clusters")
        show_figure("location_clusters.png", "15 organic neighborhoods, found via KMeans on coordinates alone.")

col5, col6 = st.columns(2)
with col5:
    with card("age-renov", accent="brass"):
        st.markdown("#### Age vs. Price, by Renovation")
        show_figure("age_vs_price_renovation.png", "Older homes alone show no clear price trend — but renovated older homes cluster higher.")
with col6:
    with card("dist-price", accent="teal"):
        st.markdown("#### Distance from Seattle vs. Price")
        show_figure("distance_vs_price.png", "Price drops fairly consistently with distance from the urban core.")

st.divider()
with card("cta", accent="moss"):
    st.markdown("#### Curious what a specific property might be worth?")
    st.write("These patterns are exactly what powers the prediction model.")
    st.page_link("pages/1_Predict.py", label="Get a Live Estimate")