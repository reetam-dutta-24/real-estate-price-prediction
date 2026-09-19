import streamlit as st
import requests
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from theme import inject_theme, render_sidebar, welcome_box, step_indicator, spec_card

st.set_page_config(page_title="Predict — King County Home Value", layout="wide")
inject_theme()
render_sidebar()

st.title("Predict a Property's Value")

KC_ZIPCODES = {
    98001: "Auburn", 98002: "Auburn", 98003: "Federal Way", 98004: "Bellevue",
    98005: "Bellevue", 98006: "Bellevue", 98007: "Bellevue", 98008: "Bellevue",
    98010: "Black Diamond", 98011: "Bothell", 98014: "Carnation", 98019: "Duvall",
    98022: "Enumclaw", 98023: "Federal Way", 98024: "Fall City", 98027: "Issaquah",
    98028: "Kenmore", 98029: "Issaquah", 98030: "Kent", 98031: "Kent", 98032: "Kent",
    98033: "Kirkland", 98034: "Kirkland", 98038: "Maple Valley", 98039: "Medina",
    98040: "Mercer Island", 98042: "Kent", 98045: "North Bend", 98047: "Pacific",
    98050: "Snoqualmie", 98051: "Ravensdale", 98052: "Redmond", 98053: "Redmond",
    98055: "Renton", 98056: "Renton", 98057: "Renton", 98058: "Renton",
    98059: "Renton", 98065: "Snoqualmie", 98070: "Vashon", 98072: "Woodinville",
    98074: "Sammamish", 98075: "Sammamish", 98077: "Woodinville", 98092: "Auburn",
    98102: "Seattle (Eastlake)", 98103: "Seattle (Fremont)", 98105: "Seattle (U District)",
    98106: "Seattle (Delridge)", 98107: "Seattle (Ballard)", 98108: "Seattle (Georgetown)",
    98109: "Seattle (South Lake Union)", 98112: "Seattle (Madison Park)",
    98115: "Seattle (Wedgwood)", 98116: "Seattle (West Seattle)",
    98117: "Seattle (Ballard)", 98118: "Seattle (Columbia City)",
    98119: "Seattle (Queen Anne)", 98122: "Seattle (Capitol Hill)",
    98125: "Seattle (Lake City)", 98126: "Seattle (West Seattle)",
    98133: "Seattle (Northgate)", 98136: "Seattle (West Seattle)",
    98144: "Seattle (Mount Baker)", 98146: "Burien", 98148: "Burien",
    98155: "Shoreline", 98166: "Burien", 98168: "Tukwila", 98177: "Shoreline",
    98178: "Renton", 98188: "Tukwila", 98198: "Des Moines", 98199: "Seattle (Magnolia)"
}
ZIP_CENTROIDS = {
    98001: (47.339, -122.267), 98002: (47.306, -122.215), 98003: (47.309, -122.316),
    98004: (47.618, -122.201), 98005: (47.610, -122.167), 98006: (47.558, -122.148),
    98007: (47.606, -122.147), 98008: (47.600, -122.116), 98010: (47.311, -122.008),
    98011: (47.762, -122.204), 98014: (47.645, -121.911), 98019: (47.740, -121.985),
    98022: (47.207, -121.964), 98023: (47.309, -122.363), 98024: (47.569, -121.892),
    98027: (47.530, -122.038), 98028: (47.757, -122.232), 98029: (47.552, -122.007),
    98030: (47.380, -122.196), 98031: (47.386, -122.176), 98032: (47.386, -122.238),
    98033: (47.677, -122.206), 98034: (47.710, -122.206), 98038: (47.386, -122.043),
    98039: (47.627, -122.234), 98040: (47.563, -122.226), 98042: (47.367, -122.116),
    98045: (47.483, -121.746), 98047: (47.257, -122.253), 98050: (47.531, -121.837),
    98051: (47.379, -121.888), 98052: (47.674, -122.121), 98053: (47.673, -122.038),
    98055: (47.470, -122.226), 98056: (47.500, -122.174), 98057: (47.478, -122.208),
    98058: (47.434, -122.146), 98059: (47.484, -122.140), 98065: (47.531, -121.837),
    98070: (47.409, -122.464), 98072: (47.760, -122.148), 98074: (47.616, -122.041),
    98075: (47.591, -122.051), 98077: (47.755, -122.075), 98092: (47.246, -122.192),
    98102: (47.635, -122.320), 98103: (47.669, -122.342), 98105: (47.663, -122.290),
    98106: (47.531, -122.351), 98107: (47.668, -122.386), 98108: (47.552, -122.312),
    98109: (47.632, -122.347), 98112: (47.632, -122.293), 98115: (47.687, -122.290),
    98116: (47.579, -122.394), 98117: (47.686, -122.375), 98118: (47.548, -122.281),
    98119: (47.637, -122.368), 98122: (47.610, -122.298), 98125: (47.719, -122.300),
    98126: (47.542, -122.375), 98133: (47.719, -122.343), 98136: (47.541, -122.393),
    98144: (47.582, -122.293), 98146: (47.497, -122.339), 98148: (47.434, -122.323),
    98155: (47.759, -122.297), 98166: (47.462, -122.354), 98168: (47.483, -122.279),
    98177: (47.734, -122.368), 98178: (47.495, -122.235), 98188: (47.443, -122.263),
    98198: (47.395, -122.316), 98199: (47.651, -122.399)
}
GRADE_LABELS = {1:"Very low", 4:"Low", 7:"Average, standard build", 9:"Very good", 11:"Custom, high quality", 13:"Mansion-grade"}
CONDITION_LABELS = {1:"Poor", 2:"Fair", 3:"Average", 4:"Good", 5:"Very good"}
VIEW_LABELS = {0:"None", 1:"Fair", 2:"Average", 3:"Good", 4:"Excellent"}

def nearest_label(d, value):
    keys = sorted(d.keys())
    return d[min(keys, key=lambda k: abs(k - value))]

DEFAULTS = {
    "predict_step": 1,
    "bedrooms": 3, "bathrooms": 2.0, "floors": 1.0,
    "sqft_living": 1800, "sqft_basement": 0, "sqft_lot": 5000,
    "grade": 7, "condition": 3, "view": 0,
    "waterfront": False, "renovated": False,
    "yr_built": 1990, "yr_renovated": 2010,
    "zipcode": 98103, "lat": 47.6062, "long": -122.3321,
}
for key, val in DEFAULTS.items():
    st.session_state.setdefault(key, val)

STEPS = ["Home Basics", "Quality & Condition", "Location", "Review"]
step_indicator(st.session_state.predict_step, STEPS)

def next_step(): st.session_state.predict_step += 1
def prev_step(): st.session_state.predict_step -= 1

if st.session_state.predict_step == 1:
    welcome_box("Home Basics", "Start with the core size and layout of the property.")
    c1, c2, c3 = st.columns(3)
    with c1: st.number_input("Bedrooms", 0, 15, key="bedrooms")
    with c2: st.number_input("Bathrooms", 0.0, 10.0, step=0.25, key="bathrooms")
    with c3: st.number_input("Floors", 1.0, 4.0, step=0.5, key="floors")
    st.slider("Living area (sqft)", 300, 8000, step=50, key="sqft_living")
    st.slider("Basement area (sqft)", 0, 3000, step=50, key="sqft_basement")
    st.slider("Lot size (sqft)", 500, 50000, step=100, key="sqft_lot")
    st.button("Next: Quality & Condition →", type="primary", on_click=next_step, use_container_width=True)

elif st.session_state.predict_step == 2:
    welcome_box("Quality & Condition", "How the property is built and maintained.")
    st.slider("Construction grade", 1, 13, key="grade")
    st.caption(nearest_label(GRADE_LABELS, st.session_state.grade))
    st.slider("Condition", 1, 5, key="condition")
    st.caption(CONDITION_LABELS[st.session_state.condition])
    st.slider("View quality", 0, 4, key="view")
    st.caption(VIEW_LABELS[st.session_state.view])
    cw1, cw2 = st.columns(2)
    with cw1: st.toggle("Waterfront property", key="waterfront")
    with cw2: st.toggle("Has been renovated", key="renovated")
    st.slider("Year built", 1900, 2024, key="yr_built")
    st.slider("Year renovated", 1950, 2024, key="yr_renovated", disabled=not st.session_state.renovated)
    b1, b2 = st.columns(2)
    with b1: st.button("← Back", on_click=prev_step, use_container_width=True)
    with b2: st.button("Next: Location →", type="primary", on_click=next_step, use_container_width=True)

elif st.session_state.predict_step == 3:
    welcome_box("Location", "Where the property is situated in King County.")
    zip_options = {f"{z} — {name}": z for z, name in sorted(KC_ZIPCODES.items(), key=lambda x: x[1])}
    default_idx = list(zip_options.values()).index(st.session_state.zipcode)
    zip_label = st.selectbox("Zipcode / Area", options=list(zip_options.keys()), index=default_idx)
    if zip_options[zip_label] != st.session_state.zipcode:
        st.session_state.zipcode = zip_options[zip_label]
        st.session_state.lat, st.session_state.long = ZIP_CENTROIDS.get(st.session_state.zipcode, (47.6062, -122.3321))
    st.caption("Location defaults to the center of this zipcode.")
    with st.expander("Adjust exact location (optional)"):
        st.number_input("Latitude", format="%.4f", key="lat")
        st.number_input("Longitude", format="%.4f", key="long")
    b1, b2 = st.columns(2)
    with b1: st.button("← Back", on_click=prev_step, use_container_width=True)
    with b2: st.button("Next: Review →", type="primary", on_click=next_step, use_container_width=True)

elif st.session_state.predict_step == 4:
    welcome_box("Review", "Confirm the details before generating your estimate.")
    s = st.session_state
    spec_card([
        ("Bedrooms", s.bedrooms), ("Bathrooms", s.bathrooms),
        ("Living area", f"{s.sqft_living:,} sqft"), ("Lot size", f"{s.sqft_lot:,} sqft"),
        ("Grade", f"{s.grade} — {nearest_label(GRADE_LABELS, s.grade)}"),
        ("Condition", CONDITION_LABELS[s.condition]),
        ("Area", KC_ZIPCODES.get(s.zipcode, "—")),
        ("Waterfront", "Yes" if s.waterfront else "No"),
    ])
    b1, b2 = st.columns(2)
    with b1: st.button("← Back", on_click=prev_step, use_container_width=True)
    with b2:
        if st.button("Get Estimate", type="primary", use_container_width=True):
            payload = {
                "bedrooms": s.bedrooms, "bathrooms": s.bathrooms, "sqft_living": s.sqft_living,
                "sqft_lot": s.sqft_lot, "floors": s.floors, "waterfront": int(s.waterfront),
                "view": s.view, "condition": s.condition, "grade": s.grade,
                "sqft_above": s.sqft_living - s.sqft_basement, "sqft_basement": s.sqft_basement,
                "yr_built": s.yr_built, "yr_renovated": s.yr_renovated if s.renovated else 0,
                "zipcode": s.zipcode, "lat": s.lat, "long": s.long,
                "sqft_living15": s.sqft_living, "sqft_lot15": s.sqft_lot,
            }
            with st.spinner("Analyzing property..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=15)
                    if response.status_code == 200:
                        st.session_state.prediction_result = response.json()
                        st.session_state.prediction_area = KC_ZIPCODES.get(s.zipcode, "—")
                        st.switch_page("pages/6_Results.py")
                    else:
                        st.error(f"Prediction failed: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend not reachable. Run `uvicorn main:app --reload` in the backend folder.")