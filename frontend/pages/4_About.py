import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, section_card_open, section_card_close

st.set_page_config(page_title="About", layout="wide")
inject_theme()
render_sidebar()

st.title("About This Project")
welcome_box("The story behind it", "Why this project exists and how it was built.")

section_card_open()
st.markdown("#### The Data")
st.write("21,613 residential sales across King County, Washington (2014–2015), including "
         "Seattle, Bellevue, and surrounding suburbs. Sourced from Kaggle's King County House Sales dataset.")
section_card_close()

section_card_open(accent="teal")
st.markdown("#### The Pipeline")
st.write("Raw data → cleaning → 80+ engineered features (temporal, geospatial, structural, "
         "interaction terms) → leakage-safe preprocessing → cross-validated model comparison → "
         "this deployed prediction tool.")
section_card_close()

section_card_open()
st.markdown("#### Built With")
st.markdown("""
<span class="badge">Python</span><span class="badge">scikit-learn</span>
<span class="badge">FastAPI</span><span class="badge">Streamlit</span>
<span class="badge">pandas</span><span class="badge">PCA</span>
""", unsafe_allow_html=True)
section_card_close()