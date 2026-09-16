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
- [x] `sale_quarter`
- [x] `sale_day_of_week`
- [x] `is_peak_season`
- [x] `decade_built`
- [x] `renovation_decade`
- [x] `sale_month_sin` / `sale_month_cos` (cyclical encoding)

### Category 2 — Size & structure ratios
### Category 2 — Size & structure ratios
- [x] `above_ratio` (sqft_above / sqft_living)
- [x] `living_sqft_diff_from_neighbors`
- [x] `lot_sqft_diff_from_neighbors`
- [x] `total_rooms_estimate`

### Category 3 — Quality / luxury signals
- [x] `is_luxury` (composite flag)
- [x] `luxury_score` (weighted composite)
- [x] `view_binary`

### Category 4 — Geospatial
- [x] `distance_to_bellevue`
- [x] KMeans neighborhood clusters (lat/long only, leakage-safe)
- [ ] Cluster avg price (DEFERRED to post-split, Stage 6/7)
- [x] 50 landmark distance features (airports, employers, universities, hospitals, parks, tourist sites, suburbs)
- [x] PCA compression of 50 landmarks → `amenity_proximity_pc1/pc2/pc3` (95%+ variance retained in 3 components)
- [x] NOTE: raw 50 distance_to_* columns excluded from model input (kept for EDA only) — only PCA components used

### Category 5 — Interaction features
- [x] `grade_x_sqft_living`
- [x] `age_x_renovated` (explicit numeric interaction)



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