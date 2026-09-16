import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, section_card_open, section_card_close

st.set_page_config(page_title="Model Insights", layout="wide")
inject_theme()
render_sidebar()

st.title("Model Insights")
welcome_box("Under the hood", "Performance, comparisons, and what the model has learned.")

section_card_open()
st.markdown("#### Status")
st.write("Model training hasn't run yet — this page will show algorithm comparisons, "
         "cross-validation scores, and feature importance once training is complete.")
st.markdown('<span class="badge">Pending: Model training</span> <span class="badge">Pending: Interpretation</span>', unsafe_allow_html=True)
section_card_close()