# Project Roadmap — King County House Price Prediction

Living document. Every stage gets checked off here before we move to the next. If it's not in this file, it doesn't happen.

---

## Stage 0 — Setup ✅
- [x] Virtual environment, .gitignore, folder structure
- [x] requirements.txt
- [x] README.md
- [x] Git repo initialized, connected to GitHub

## Stage 1 — Dataset Selection ✅
- [x] Evaluated California Housing, Ames, King County
- [x] Selected King County House Sales (21,613 rows, 21 features, has lat/long)

## Stage 2 — EDA ✅
- [x] `.info()`, `.describe()`, shape, missing value check
- [x] Target distribution (`price`) — confirmed right-skew
- [x] Log-transform target → `log_price`
- [x] Correlation heatmap — flagged multicollinearity cluster
- [x] Geospatial scatter (lat/long colored by price)

## Stage 3 — Data Cleaning ✅
- [x] Dropped `Unnamed: 0`, `id`
- [x] Converted `date` → datetime, extracted `sale_year`, `sale_month`
- [x] Median-imputed missing `bedrooms` (13), `bathrooms` (10)
- [x] Verified no duplicates
- [x] Fixed 33-bedroom data entry error → 3
- [x] Verified 9-11 bedroom homes are legitimate (checked against sqft)

## Stage 4 — Feature Engineering (IN PROGRESS)

### Built already
- [x] `sale_year`, `sale_month`
- [x] `house_age`
- [x] `was_renovated`, `years_since_renovation`
- [x] `has_basement`
- [x] `distance_to_seattle` (haversine)
- [x] `sqft_ratio`, `bed_bath_ratio`
- [x] `log_price`

### Category 1 — Temporal
- [ ] `sale_quarter`
- [ ] `sale_day_of_week`
- [ ] `is_peak_season`
- [ ] `decade_built`
- [ ] `renovation_decade`
- [ ] `sale_month_sin` / `sale_month_cos` (cyclical encoding)

### Category 2 — Size & structure ratios
- [ ] `above_ratio` (sqft_above / sqft_living)
- [ ] `living_sqft_diff_from_neighbors`
- [ ] `lot_sqft_diff_from_neighbors`
- [ ] `total_rooms_estimate`

### Category 3 — Quality / luxury signals
- [ ] `is_luxury` (composite flag)
- [ ] `luxury_score` (weighted composite)
- [ ] `view_binary`

### Category 4 — Geospatial
- [ ] `distance_to_bellevue`
- [ ] KMeans neighborhood clusters + cluster avg price (post-split, train-only)

### Category 5 — Interaction features
- [ ] `grade_x_sqft_living`
- [ ] `age_x_renovated` (explicit numeric interaction)

### Display-only (NOT for model)
- [ ] `city_name` via `pgeocode` (zipcode → readable location, for UI only)

### ⚠️ Explicitly avoided
- [x] Decided AGAINST `price_per_sqft` as input feature — direct target leakage

## Stage 5 — Preprocessing Decisions (PENDING)
- [ ] Skew check on `sqft_living`, `sqft_lot`, `sqft_above`, `sqft_basement` → log-transform if needed
- [ ] Multicollinearity — compute VIF, decide keep/drop
- [ ] Outlier strategy — winsorize vs keep raw
- [ ] Scaler choice — StandardScaler vs RobustScaler (leaning RobustScaler)
- [ ] lat/long — keep raw alongside distance features? (decision pending)
- [ ] Confirm `grade`/`condition`/`view` stay ordinal (not one-hot)
- [ ] Zipcode encoding strategy — target encoding (leakage-safe, post-split)

## Stage 6 — Data Splitting (PENDING — BLOCKING)
- [ ] Decide: train/val/test (3-way) vs train/test + cross-validation
- [ ] Implement `split_data()` in `src/preprocess.py`

## Stage 7 — Build the Pipeline
- [ ] `ColumnTransformer` (numeric scaling + categorical encoding)
- [ ] Wrap in `sklearn.Pipeline`
- [ ] Verify no leakage (fit only on train)

## Stage 8 — Baseline Model
- [ ] Dumb baseline (predict mean) — establish the floor to beat

## Stage 9 — Model Training
- [ ] Linear Regression (baseline-ish)
- [ ] Random Forest
- [ ] Gradient Boosting (XGBoost / LightGBM)

## Stage 10 — Evaluation
- [ ] RMSE, MAE, R² across models
- [ ] Cross-validation scores
- [ ] Residual analysis

## Stage 11 — Hyperparameter Tuning
- [ ] GridSearch / RandomSearch / Optuna

## Stage 12 — Model Interpretation
- [ ] Feature importance
- [ ] SHAP values

## Stage 13 — Experiment Tracking
- [ ] MLflow setup, log experiments

## Stage 14 — Serialization
- [ ] Save final pipeline + model (joblib)

## Stage 15 — Backend API
- [ ] FastAPI service, `/predict` endpoint

## Stage 16 — Frontend UI
- [ ] Streamlit app — form input, map visualization, prediction display

## Stage 17 — Deployment
- [ ] Deploy backend + frontend (Render/Railway/HF Spaces)

## Stage 18 — Documentation & Polish
- [ ] `reports/feature_dictionary.md` — every feature explained
- [ ] Final README polish with visuals + live demo link
- [ ] Model report (`reports/model_report.md`)

---

## Git checkpoint convention
Commit + push at the end of every numbered stage above. No exceptions.