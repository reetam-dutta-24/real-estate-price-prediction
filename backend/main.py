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

FRIENDLY_NAMES = {
    'zipcode_encoded': 'Neighborhood price level',
    'cluster_avg_price': 'Local area pricing',
    'grade_x_sqft_living': 'Size & build quality combined',
    'luxury_score': 'Luxury features',
    'sqft_living_log': 'Living area',
    'is_luxury': 'Luxury property status',
    'lat': 'Latitude position',
    'long': 'Longitude position',
    'view': 'View quality',
    'waterfront': 'Waterfront access',
    'grade': 'Construction grade',
    'condition': 'Property condition',
    'house_age': 'Age of home',
    'was_renovated': 'Renovation status',
    'amenity_proximity_pc1': 'Proximity to amenities',
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
        idx_sorted = np.argsort(-np.abs(shap_vals))[:5]
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

        return {
            "predicted_price": round(pred_dollar),
            "note": "Tuned XGBoost model — test R² 0.91",
            "factors": factors
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))