# King County Home Value Predictor

An end-to-end machine learning project predicting residential real estate prices in King County, Washington (Seattle metro area) — from raw data through feature engineering, leakage-safe preprocessing, model training, and a deployed full-stack prediction tool.

## Project Overview

This project builds a regression pipeline to estimate King County home prices using 21,613 real sale records from 2014–2015. Beyond a standard regression exercise, the focus is on **doing the full ML lifecycle properly**: rigorous exploratory analysis, deliberate feature engineering (100+ derived columns), leakage-aware preprocessing decisions backed by statistical reasoning (VIF, skew analysis), and a working application layer — not just a notebook that stops at `.fit()`.

## Dataset

- **Source:** [King County House Sales — Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)
- **Size:** 21,613 rows, 21 raw columns
- **Why this dataset:** Chosen over more commonly used options (California Housing, Ames) specifically for its `lat`/`long` coordinates — enabling real geospatial feature engineering and an interactive map-based UI, which most beginner real estate projects skip entirely.

## Key Findings from EDA

- **Price is heavily right-skewed** (skew ≈ high, long tail toward $7–8M luxury properties) — addressed via log-transformation of the target (`log_price`)
- **Location is the dominant price driver** — properties cluster tightly in price by proximity to Seattle/Bellevue and along Lake Washington waterfront
- **House age alone shows no clear price trend** — but splitting by renovation status reveals renovated older homes cluster at meaningfully higher prices, showing why `was_renovated` was engineered as its own feature rather than relying on age alone
- **Severe multicollinearity** identified via VIF between `sqft_living`, `sqft_above`, and related size columns (VIF > 26) — `sqft_above` dropped from the final feature set as a result

## Feature Engineering

Starting from 21 raw columns, ~100+ features were engineered across these categories:

| Category | Examples |
|---|---|
| Temporal | `house_age`, `sale_quarter`, cyclical month encoding (`sale_month_sin/cos`), `decade_built` |
| Size & structure | `above_ratio`, neighbor-relative size comparisons, `total_rooms_estimate` |
| Quality signals | `is_luxury`, `luxury_score`, `view_binary` |
| Geospatial | `distance_to_seattle`, `distance_to_bellevue`, KMeans-derived `location_cluster` (15 organic neighborhoods), 50 landmark distances compressed to 3 features via PCA |
| Interactions | `grade_x_sqft_living`, `age_x_renovated` |

**50 landmark distances → 3 PCA components:** rather than feeding 50 highly-correlated raw distance features into the model, PCA analysis showed 3 components retain 95%+ of the variance — a deliberate dimensionality-reduction step to avoid feature redundancy while preserving the signal.

## Preprocessing Decisions

Every preprocessing choice was made deliberately, not by default:

- **Log-transformation** applied to price and skewed size columns (skew reduced from up to 13.0 down to under 1.0)
- **RobustScaler** chosen over StandardScaler — median/IQR-based scaling resists distortion from genuine luxury-property outliers, which were deliberately kept in the dataset (not winsorized) rather than deleted
- **Zipcode target encoding**, computed strictly on training data post-split to prevent data leakage
- **Ordinal features** (`grade`, `condition`, `view`) left as plain numeric — one-hot encoding would have destroyed their meaningful ordering
- **80/20 train/test split** with 5-fold cross-validation used for model comparison and tuning — no fixed validation set, maximizing use of a moderate-sized dataset

## Project Structure
housing/
├── data/
│ ├── raw/ # Original Kaggle CSV
│ └── processed/ # Cleaned/transformed data
├── notebooks/
│ ├── 01_eda.ipynb # Exploratory analysis
│ └── 02_preprocessing.ipynb
├── src/
│ └── preprocess.py # Reusable cleaning, feature engineering, and split pipeline
├── models/ # Saved trained model (pending)
├── reports/
│ └── figures/ # Saved EDA visualizations
├── backend/ # FastAPI prediction API
├── frontend/ # Streamlit multi-page application
├── requirements.txt
└── PROJECT_ROADMAP.md # Full stage-by-stage build log


## Tech Stack

- **Data & ML:** Python, pandas, NumPy, scikit-learn, statsmodels
- **Visualization:** matplotlib, seaborn
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Geospatial:** custom haversine distance calculations, KMeans clustering, pgeocode

## Setup

```bash
git clone https://github.com/reetam-dutta-24/real-estate-price-prediction
cd real-estate-price-prediction
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Download `kc_house_data.csv` from the [dataset source](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction) and place it in `data/raw/`.

## Running the App

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
streamlit run app.py
```

## Status

🚧 **In progress.** See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for the full stage-by-stage build log.

- [x] EDA & data cleaning
- [x] Feature engineering (100+ features)
- [x] Preprocessing decisions (skew, VIF, scaling, encoding strategy)
- [x] Train/test split
- [x] Frontend scaffold (Streamlit, multi-page)
- [x] Backend scaffold (FastAPI, placeholder endpoint)
- [ ] Leakage-safe zipcode/cluster encoding implementation
- [ ] Preprocessing pipeline (ColumnTransformer)
- [ ] Model training & comparison
- [ ] Hyperparameter tuning
- [ ] Model interpretation (feature importance, SHAP)
- [ ] Full backend/frontend integration with trained model
- [ ] Deployment


