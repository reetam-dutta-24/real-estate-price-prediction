import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, skeleton_lines

st.set_page_config(page_title="Predict — King County Home Value", layout="wide")
inject_theme()
render_sidebar()

st.title("Predict a Property's Value")
welcome_box("Get an estimate", "Fill in the property details below and set its location on the map to generate a price estimate.")

col_form, col_map = st.columns([1, 1.1])

with col_form:
    c1, c2 = st.columns(2)
    with c1:
        bedrooms = st.number_input("Bedrooms", 0, 15, 3)
        bathrooms = st.number_input("Bathrooms", 0.0, 10.0, 2.0, step=0.25)
        floors = st.number_input("Floors", 1.0, 4.0, 1.0, step=0.5)
        grade = st.slider("Construction grade (1–13)", 1, 13, 7)
    with c2:
        sqft_living = st.number_input("Living area (sqft)", 200, 15000, 1800)
        sqft_lot = st.number_input("Lot size (sqft)", 500, 200000, 5000)
        condition = st.slider("Condition (1–5)", 1, 5, 3)
        view = st.slider("View quality (0–4)", 0, 4, 0)

    waterfront = st.checkbox("Waterfront property")
    yr_built = st.number_input("Year built", 1900, 2024, 1990)
    renovated = st.checkbox("Renovated")
    yr_renovated = st.number_input("Year renovated", 1900, 2024, 2000, disabled=not renovated)

    st.markdown("**Location**")
    lat = st.number_input("Latitude", value=47.6062, format="%.4f")
    long = st.number_input("Longitude", value=-122.3321, format="%.4f")

    predict_clicked = st.button("Predict Price", type="primary", use_container_width=True)

with col_map:
    st.markdown("**Property Location**")
    map_df = pd.DataFrame({'lat': [lat], 'lon': [long]})
    view_state = pdk.ViewState(latitude=lat, longitude=long, zoom=11)
    layer = pdk.Layer("ScatterplotLayer", data=map_df, get_position='[lon, lat]',
                       get_color='[169, 120, 47, 200]', get_radius=300)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="road"))

st.divider()
result_area = st.empty()

if predict_clicked:
    with result_area.container():
        skeleton_lines(2)

    payload = {"sqft_living": sqft_living, "bedrooms": bedrooms, "bathrooms": bathrooms,
               "grade": grade, "lat": lat, "long": long}
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
        result = response.json()
        with result_area.container():
            st.markdown(f"### Estimated Price: ${result['predicted_price']:,.0f}")
            st.caption(result.get("note", ""))
    except requests.exceptions.ConnectionError:
        with result_area.container():
            st.error("Backend not reachable. Run `uvicorn main:app --reload` in the backend folder.")