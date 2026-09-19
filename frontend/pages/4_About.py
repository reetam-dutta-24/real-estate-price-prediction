import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, card, list_row

st.set_page_config(page_title="About", layout="wide")
inject_theme()
render_sidebar()

st.title("About This Project")
welcome_box("The story behind it", "An end-to-end machine learning project — from raw data to a deployed, explainable prediction tool.")

col1, col2 = st.columns(2)

with col1:
    with card("data", accent="brass"):
        st.markdown("#### The Data")
        st.write("21,613 residential sales across King County, Washington (2014–2015), including "
                 "Seattle, Bellevue, and surrounding suburbs. Sourced from Kaggle's King County House Sales dataset.")

    with card("pipeline", accent="teal"):
        st.markdown("#### The Pipeline")
        st.write("Raw data → cleaning → 100+ engineered features (temporal, geospatial, structural, "
                 "interaction terms) → leakage-safe preprocessing → cross-validated model comparison → "
                 "hyperparameter tuning → this deployed, explainable prediction tool.")

    with card("different", accent="moss"):
        st.markdown("#### What Makes This Different")
        st.write("Most beginner projects stop at reporting an accuracy score. This one documents and "
                 "justifies every preprocessing decision (VIF analysis, skew correction, leakage-safe "
                 "target encoding), explains the model's own reasoning per-prediction via SHAP, and runs "
                 "as a real, live application.")

with col2:
    with card("architecture", accent="clay"):
        st.markdown("#### Architecture")
        list_row("Data pipeline", "src/preprocess.py", "Python")
        list_row("Model training", "src/train.py", "scikit-learn, XGBoost")
        list_row("Experiment tracking", "MLflow, SQLite backend", "5 tracked runs")
        list_row("Backend API", "FastAPI", "/predict endpoint")
        list_row("Frontend", "Streamlit, multi-page", "Custom theme")
        list_row("Interpretability", "SHAP", "Per-prediction explanations")

    with card("performance", accent="brass"):
        st.markdown("#### Model Performance")
        list_row("Test R²", "Tuned XGBoost", "0.9148")
        list_row("Test MAE", "Median dollar error", "$62,141")
        list_row("vs. Baseline", "Error reduction", "71%")

    with card("built-with", accent="teal"):
        st.markdown("#### Built With")
        st.markdown("""
        <span class="badge">Python</span><span class="badge">scikit-learn</span>
        <span class="badge">XGBoost</span><span class="badge">SHAP</span>
        <span class="badge">MLflow</span><span class="badge">FastAPI</span>
        <span class="badge">Streamlit</span><span class="badge">pandas</span>
        <span class="badge">PCA</span><span class="badge">pydeck</span>
        """, unsafe_allow_html=True)

st.divider()
with card("source", accent="moss"):
    st.markdown("#### Source")
    st.write("Full source code, notebooks, and documentation available on GitHub.")
    st.link_button("View on GitHub", "https://github.com/reetam-dutta-24/real-estate-price-prediction")