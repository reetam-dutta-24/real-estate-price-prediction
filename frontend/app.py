import streamlit as st
import requests

st.title("🏠 King County House Price Predictor")
st.write("Enter house details to get a predicted price.")

sqft_living = st.number_input("Living Area (sqft)", min_value=200, max_value=15000, value=1800)
bedrooms = st.number_input("Bedrooms", min_value=0, max_value=15, value=3)
bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.25)
grade = st.slider("Construction Grade (1-13)", 1, 13, 7)
lat = st.number_input("Latitude", value=47.6062, format="%.4f")
long = st.number_input("Longitude", value=-122.3321, format="%.4f")

if st.button("Predict Price"):
    payload = {
        "sqft_living": sqft_living,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "grade": grade,
        "lat": lat,
        "long": long,
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    result = response.json()
    st.success(f"Predicted Price: ${result['predicted_price']:,.0f}")
    st.caption(result['note'])