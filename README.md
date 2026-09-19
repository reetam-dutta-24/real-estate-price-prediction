# King County Home Value Predictor

🔗 **Live demo:** [kc-home-value.streamlit.app](https://kc-home-value.streamlit.app)
🔗 **API docs:** [kc-house-price-api.onrender.com/docs](https://kc-house-price-api.onrender.com/docs)

> The backend runs on a free-tier server that sleeps after ~15 minutes of inactivity. The first prediction after idle may take 30–60 seconds to respond while it wakes up — subsequent requests are fast.

An end-to-end machine learning project predicting residential real estate prices in King County, Washington (Seattle metro area) — from raw data through feature engineering, leakage-safe preprocessing, model training, and a deployed, explainable prediction application.

## Project Overview

This project builds a regression pipeline to estimate King County home prices using 21,613 real sale records from 2014–2015. Beyond a standard regression exercise, the focus is on doing the full ML lifecycle properly: rigorous exploratory analysis, deliberate feature engineering (100+ derived columns), leakage-aware preprocessing decisions backed by statistical reasoning (VIF, skew analysis), a tuned and interpretable model, and a genuinely functional full-stack application — not a notebook that stops at `.fit()`.

## Live Application

A four-step guided form collects property details, sends them to a live FastAPI backend running the trained model, and returns a full valuation report: estimated price with a confidence range, a SHAP-based breakdown of what's driving the estimate, comparable nearby sales, neighborhood statistics, and a pinned map of nearby amenities.

## Dataset

- **Source:** [King County House Sales — Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)
- **Size:** 21,613 rows, 21 raw columns, 2014–2015 sales
- **Why this dataset:** Selected over more commonly used options (California Housing, Ames) specifically for its `lat`/`long` coordinates — enabling real geospatial feature engineering and an interactive, map-based application, which most beginner real estate projects skip.

## Key Findings from EDA

- **Price is heavily right-skewed** (skew ≈ high, long tail toward $7–8M luxury properties) — addressed via log-transformation of the target
- **Location is the dominant price driver** — properties cluster tightly in price by proximity to Seattle/Bellevue and along Lake Washington waterfront
- **House age alone shows no clear price trend** — but splitting by renovation status reveals renovated older homes cluster at meaningfully higher prices, motivating dedicated renovation features rather than relying on age alone
- **Severe multicollinearity** identified via VIF between `sqft_living`, `sqft_above`, and related size columns (VIF > 26) — `sqft_above` dropped from the final feature set

## Feature Engineering

Starting from 21 raw columns, 100+ features were engineered across five categories — full definitions in [`reports/feature_dictionary.md`](reports/feature_dictionary.md):

| Category | Examples |
|---|---|
| Temporal | `house_age`, `sale_quarter`, cyclical month encoding, `decade_built` |
| Size & structure | `above_ratio`, neighbor-relative size comparisons, `total_rooms_estimate` |
| Quality signals | `is_luxury`, `luxury_score`, `view_binary` |
| Geospatial | `distance_to_seattle`/`bellevue`, KMeans `location_cluster` (15 organic neighborhoods), 50 landmark distances compressed to 3 features via PCA |
| Interactions | `grade_x_sqft_living`, `age_x_renovated` |

**50 landmark distances → 3 PCA components:** rather than feeding 50 highly-correlated raw distance features into the model, explained-variance analysis showed 3 PCA components retain 95%+ of the signal — a deliberate dimensionality-reduction step to avoid redundancy while preserving predictive value.

## Preprocessing Decisions

Every preprocessing choice was made deliberately and documented — see [`PROJECT_ROADMAP.md`](PROJECT_ROADMAP.md) for the full reasoning behind each:

- **Log-transformation** on price and skewed size columns (skew reduced from up to 13.0 to under 1.0)
- **RobustScaler** over StandardScaler — resists distortion from genuine luxury-property outliers, which were deliberately kept in the dataset rather than winsorized or deleted
- **Zipcode and location-cluster target encoding**, computed strictly on training data post-split to prevent leakage
- **Ordinal features** (`grade`, `condition`, `view`) kept as plain numeric — one-hot encoding would destroy their meaningful order
- **80/20 train/test split** with 5-fold cross-validation for model comparison and tuning — no fixed validation set, maximizing use of a moderate-sized dataset

## Model Performance

| Model | Test RMSE (log) | Test MAE ($) | Test R² |
|---|---|---|---|
| Baseline (mean) | 0.5340 | $229,795 | ~0.00 |
| Linear Regression | 0.1757 | $75,884 | 0.87 |
| Random Forest | 0.1710 | $68,481 | 0.89 |
| XGBoost (default) | 0.1663 | $66,631 | 0.90 |
| **XGBoost (tuned)** | **0.1558** | **$62,141** | **0.9148** |

The final tuned XGBoost model (found via `RandomizedSearchCV`, 30 candidates × 5-fold CV) explains ~91% of price variance and reduces error by 71% versus a naive baseline. Full analysis in [`reports/model_report.md`](reports/model_report.md).

**Interpretability:** feature importance and SHAP analysis confirm the model's top predictors are the engineered features — zipcode encoding, luxury signals, and the grade×living-area interaction — rather than raw columns alone, validating the feature engineering effort. Residual analysis shows the model is most precise on mainstream housing (<$1M), with reduced precision on the sparser, higher-variance luxury segment — an honest, documented limitation rather than a hidden weakness.

## Project Structure
housing/
├── data/
│ ├── raw/ # Original Kaggle CSV
│ └── processed/ # Cleaned/transformed data
├── notebooks/
│ ├── 01_eda.ipynb # Exploratory analysis
│ ├── 02_preprocessing.ipynb # Pipeline construction & validation
│ └── 03_modeling.ipynb # Training, tuning, interpretation
├── src/
│ ├── preprocess.py # Cleaning, feature engineering, pipeline
│ └── train.py # Baseline, model comparison, tuning
├── models/ # Serialized model, preprocessor, KMeans, PCA
├── reports/
│ ├── figures/ # Saved EDA and model visualizations
│ ├── feature_dictionary.md # Every feature, defined
│ └── model_report.md # Full performance write-up
├── backend/ # FastAPI prediction API
├── frontend/ # Streamlit multi-page application
├── requirements.txt
└── PROJECT_ROADMAP.md # Full stage-by-stage build log



## Tech Stack

- **Data & ML:** Python, pandas, NumPy, scikit-learn, XGBoost, statsmodels
- **Interpretability:** SHAP
- **Experiment tracking:** MLflow (SQLite backend)
- **Visualization:** matplotlib, seaborn
- **Backend:** FastAPI
- **Frontend:** Streamlit (multi-page, custom theme, pydeck maps)
- **Geospatial:** haversine distance calculations, KMeans clustering, pgeocode
- **Deployment:** Render (backend), Streamlit Community Cloud (frontend)

## Running Locally

```bash
git clone https://github.com/reetam-dutta-24/real-estate-price-prediction
cd real-estate-price-prediction
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Download `kc_house_data.csv` from the [dataset source](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction) and place it in `data/raw/`.

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The frontend defaults to calling the backend at `http://127.0.0.1:8000`. To point it elsewhere, set the `BACKEND_URL` environment variable.

## Status

✅ **Complete and deployed.**

- [x] EDA, cleaning, feature engineering (100+ features)
- [x] Leakage-safe preprocessing pipeline
- [x] Model training, comparison, and hyperparameter tuning
- [x] SHAP interpretability, MLflow experiment tracking
- [x] Serialized model, FastAPI backend, Streamlit frontend
- [x] Deployed live (Render + Streamlit Community Cloud)

See [`PROJECT_ROADMAP.md`](PROJECT_ROADMAP.md) for the full stage-by-stage build log, [`reports/feature_dictionary.md`](reports/feature_dictionary.md) for feature definitions, and [`reports/model_report.md`](reports/model_report.md) for complete model performance details.

