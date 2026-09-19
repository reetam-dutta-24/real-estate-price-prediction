import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, stat_strip, card, metric_table, FIGURES_DIR

st.set_page_config(page_title="Model Insights", layout="wide")
inject_theme()
render_sidebar()

st.title("Model Insights")
welcome_box("Under the hood", "How the model was built, tuned, and evaluated — and what it actually learned.")

stat_strip([
    ("0.9148", "Test R²"),
    ("$62,141", "Test MAE"),
    ("71%", "vs. baseline"),
    ("150", "Tuning fits"),
])

with card("comparison-table", accent="brass"):
    st.markdown("#### Model Comparison")
    metric_table([
        {"model": "Baseline (mean)", "rmse": "0.5340", "mae": "$229,795", "r2": "~0.00"},
        {"model": "Linear Regression", "rmse": "0.1757", "mae": "$75,884", "r2": "0.87"},
        {"model": "Random Forest", "rmse": "0.1710", "mae": "$68,481", "r2": "0.89"},
        {"model": "XGBoost (default)", "rmse": "0.1663", "mae": "$66,631", "r2": "0.90"},
        {"model": "XGBoost (tuned)", "rmse": "0.1558", "mae": "$62,141", "r2": "0.9148"},
    ], highlight_label="XGBoost (tuned)")
    st.caption("Models compared via 5-fold cross-validation; final numbers are a single held-out test-set evaluation.")


def show_figure(filename, caption):
    path = os.path.join(FIGURES_DIR, filename)
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"Figure not found: {filename}")


col1, col2 = st.columns(2)
with col1:
    with card("importance", accent="teal"):
        st.markdown("#### What Drives Predictions")
        show_figure("feature_importance.png", "Zipcode encoding, luxury signals, and size×grade interactions dominate.")
with col2:
    with card("shap", accent="moss"):
        st.markdown("#### SHAP: Direction of Effect")
        show_figure("shap_summary.png", "Confirms the model learned sensible real-world relationships.")

with card("residuals", accent="clay"):
    st.markdown("#### Where the Model Struggles")
    show_figure("residuals_vs_predicted.png", "Error grows with price — the model is most precise on the mainstream market.")
    st.write("Residual analysis shows the model performs strongly on homes under $1M, with reduced "
             "precision on luxury properties — consistent with their sparser representation and higher "
             "price variance in the training data.")