import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, FIGURES_DIR, section_card_open, section_card_close

st.set_page_config(page_title="Market Explorer", layout="wide")
inject_theme()
render_sidebar()

st.title("Market Explorer")
welcome_box("Explore the data", "Findings from exploratory analysis of 21,613 King County home sales.")


def show_figure(filename, caption):
    path = os.path.join(FIGURES_DIR, filename)
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"Figure not generated yet: {filename}")


col1, col2 = st.columns(2)
with col1:
    section_card_open()
    st.markdown("#### Price Distribution")
    show_figure("price_distribution.png", "Right-skewed — most homes cluster $300K–$600K, with a long luxury tail.")
    section_card_close()

with col2:
    section_card_open(accent="teal")
    st.markdown("#### Geography of Price")
    show_figure("geo_price_map.png", "Price by location — waterfront and central areas command a premium.")
    section_card_close()

col3, col4 = st.columns(2)
with col3:
    section_card_open()
    st.markdown("#### Feature Correlation")
    show_figure("correlation_heatmap.png", "sqft_living, grade, and bathrooms move together — addressed via VIF.")
    section_card_close()

with col4:
    section_card_open(accent="teal")
    st.markdown("#### Geographic Clusters")
    show_figure("location_clusters.png", "15 organic neighborhoods, found via KMeans on coordinates alone.")
    section_card_close()