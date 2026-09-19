import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import shap
from src import preprocess

app = FastAPI(title="House Price Prediction API")

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
preprocessor = joblib.load(os.path.join(MODELS_DIR, "preprocessor.pkl"))
model = joblib.load(os.path.join(MODELS_DIR, "xgb_model.pkl"))
kmeans_model = joblib.load(os.path.join(MODELS_DIR, "kmeans_model.pkl"))
pca_model = joblib.load(os.path.join(MODELS_DIR, "pca_model.pkl"))
pca_scaler = joblib.load(os.path.join(MODELS_DIR, "pca_scaler.pkl"))

explainer = shap.TreeExplainer(model)
FEATURE_NAMES = preprocessor.get_feature_names_out()

REFERENCE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "kc_house_data_NaN.csv")
_df = preprocess.load_data(REFERENCE_DATA_PATH)
_df = preprocess.clean_data(_df)
_df, _, _, _ = preprocess.engineer_features(_df, kmeans_model=kmeans_model, pca_model=pca_model, pca_scaler=pca_scaler)
ZIPCODE_MAP = _df.groupby('zipcode')['log_price'].mean()
CLUSTER_MAP = _df.groupby('location_cluster')['log_price'].mean()
OVERALL_MEAN = _df['log_price'].mean()

# Known final evaluation numbers from Stage 9-11 (see PROJECT_ROADMAP.md)
TEST_MAE_DOLLAR = 62141

FRIENDLY_NAMES = {
    'zipcode_encoded': 'Neighborhood price level', 'cluster_avg_price': 'Local area pricing',
    'grade_x_sqft_living': 'Size & build quality combined', 'luxury_score': 'Luxury features',
    'sqft_living_log': 'Living area', 'is_luxury': 'Luxury property status',
    'lat': 'Latitude position', 'long': 'Longitude position', 'view': 'View quality',
    'waterfront': 'Waterfront access', 'grade': 'Construction grade', 'condition': 'Property condition',
    'house_age': 'Age of home', 'was_renovated': 'Renovation status',
    'amenity_proximity_pc1': 'Proximity to amenities', 'sqft_lot_log': 'Lot size',
    'bathrooms': 'Bathroom count', 'bedrooms': 'Bedroom count',
}

LANDMARK_CATEGORY = {
    'seatac_airport': 'Airport', 'boeing_field': 'Airport', 'university_of_washington_station': 'Transit',
    'amazon_hq_seattle': 'Employer', 'microsoft_redmond': 'Employer', 'boeing_everett': 'Employer',
    'google_kirkland': 'Employer', 'expedia_seattle': 'Employer',
    'university_of_washington': 'Education', 'seattle_university': 'Education', 'bellevue_college': 'Education',
    'harborview_medical_center': 'Hospital', 'uw_medical_center': 'Hospital',
    'seattle_childrens_hospital': 'Hospital', 'overlake_medical_center': 'Hospital',
    'evergreen_health_medical_center': 'Hospital',
    'pike_place_market': 'Downtown', 'downtown_bellevue': 'Downtown', 'downtown_kirkland': 'Downtown',
    'downtown_redmond': 'Downtown', 'downtown_renton': 'Downtown', 'downtown_kent': 'Downtown',
    'downtown_auburn': 'Downtown', 'downtown_issaquah': 'Downtown',
    'bellevue_square': 'Shopping', 'westfield_southcenter': 'Shopping', 'alderwood_mall': 'Shopping',
    'discovery_park': 'Park', 'woodland_park_zoo': 'Park', 'alki_beach': 'Park',
    'lake_sammamish': 'Recreation', 'lake_washington_kirkland': 'Recreation', 'cougar_mountain': 'Park',
    'mercer_slough_nature_park': 'Park', 'gene_coulon_park': 'Park',
    'space_needle': 'Landmark', 'seattle_art_museum': 'Landmark', 'climate_pledge_arena': 'Landmark',
    'lumen_field': 'Landmark', 't_mobile_park': 'Landmark', 'chihuly_garden_and_glass': 'Landmark',
    'downtown_shoreline': 'Suburb', 'downtown_federal_way': 'Suburb', 'downtown_burien': 'Suburb',
    'mercer_island_town_center': 'Suburb', 'downtown_tukwila': 'Suburb', 'sammamish_town_center': 'Suburb',
    'newcastle_wa': 'Suburb', 'north_bend_wa': 'Suburb', 'vashon_island': 'Suburb', 'snoqualmie_falls': 'Recreation',
}


def get_nearest_landmarks(lat, long, top_n=8):
    results = []
    for key, (llat, llon) in preprocess.LANDMARKS.items():
        d = preprocess.haversine_distance(lat, long, llat, llon)
        results.append({
            "name": key.replace("_", " ").title(),
            "category": LANDMARK_CATEGORY.get(key, "Landmark"),
            "distance_km": round(float(d), 2),
            "lat": llat, "long": llon
        })
    results.sort(key=lambda x: x["distance_km"])
    return results[:top_n]


def get_comparables(lat, long, bedrooms, top_n=5):
    d = preprocess.haversine_distance(_df['lat'].values, _df['long'].values, lat, long)
    tmp = _df.copy()
    tmp['distance_km'] = d
    tmp = tmp.sort_values('distance_km').head(60)
    tmp['bed_diff'] = (tmp['bedrooms'] - bedrooms).abs()
    tmp = tmp.sort_values(['bed_diff', 'distance_km']).head(top_n)
    return tmp[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'distance_km']].round(2).to_dict('records')


def get_neighborhood_stats(zipcode):
    sub = _df[_df['zipcode'] == zipcode]
    if len(sub) == 0:
        return None
    return {
        "avg_price": round(float(sub['price'].mean())),
        "avg_sqft": round(float(sub['sqft_living'].mean())),
        "sale_count": int(len(sub))
    }


class HouseFeatures(BaseModel):
    bedrooms: int
    bathrooms: float
    sqft_living: int
    sqft_lot: int
    floors: float
    waterfront: int = 0
    view: int = 0
    condition: int
    grade: int
    sqft_above: int
    sqft_basement: int = 0
    yr_built: int
    yr_renovated: int = 0
    zipcode: int
    lat: float
    long: float
    sqft_living15: int
    sqft_lot15: int
    sale_year: int = 2024
    sale_month: int = 6


@app.get("/")
def root():
    return {"message": "House Price Prediction API is running"}


@app.post("/predict")
def predict(features: HouseFeatures):
    try:
        row = pd.DataFrame([features.dict()])
        row['date'] = pd.to_datetime(f"{features.sale_year}-{features.sale_month:02d}-01")

        row, _, _, _ = preprocess.engineer_features(
            row, kmeans_model=kmeans_model, pca_model=pca_model, pca_scaler=pca_scaler, add_city=False
        )

        row['zipcode_encoded'] = row['zipcode'].map(ZIPCODE_MAP).fillna(OVERALL_MEAN)
        row['cluster_avg_price'] = row['location_cluster'].map(CLUSTER_MAP).fillna(OVERALL_MEAN)
        row = row.drop(columns=['zipcode'])

        model_cols = preprocessor.feature_names_in_
        row = row.reindex(columns=model_cols, fill_value=0)

        row_processed = preprocessor.transform(row)
        pred_log = model.predict(row_processed)
        pred_dollar = float(np.expm1(pred_log[0]))

        shap_vals = explainer.shap_values(row_processed)[0]
        idx_sorted = np.argsort(-np.abs(shap_vals))[:8]
        max_abs = np.abs(shap_vals[idx_sorted]).max() or 1

        factors = []
        for i in idx_sorted:
            raw_name = FEATURE_NAMES[i].split("__")[-1]
            label = FRIENDLY_NAMES.get(raw_name, raw_name.replace("_", " ").title())
            factors.append({
                "label": label,
                "direction": "up" if shap_vals[i] > 0 else "down",
                "magnitude": float(abs(shap_vals[i]) / max_abs)
            })

        percentile = float((_df['price'] < pred_dollar).mean() * 100)

        return {
            "county_median_price": round(float(_df['price'].median())),
            "predicted_price": round(pred_dollar),
            "price_low": round(pred_dollar - TEST_MAE_DOLLAR),
            "price_high": round(pred_dollar + TEST_MAE_DOLLAR),
            "price_per_sqft": round(pred_dollar / max(features.sqft_living, 1)),
            "percentile": round(percentile, 1),
            "note": "Tuned XGBoost model — test R² 0.91",
            "factors": factors,
            "neighborhood": get_neighborhood_stats(features.zipcode),
            "comparables": get_comparables(features.lat, features.long, features.bedrooms),
            "nearby_landmarks": get_nearest_landmarks(features.lat, features.long),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))