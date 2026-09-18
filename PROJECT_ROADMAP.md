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

## Stage 5 — Preprocessing Decisions (IN PROGRESS)
- [x] Skew check on sqft_living, sqft_lot, sqft_above, sqft_basement (+ sqft_living15, sqft_lot15)
- [x] Log-transformed all 6 → sqft_*_log versions (skew reduced from up to 13.06 down to under 1.0)
- [x] NOTE: original (non-log) sqft columns excluded from X at Stage 6 — use _log versions
- [x] Multicollinearity — VIF computed. sqft_living_log & sqft_above_log both >26 (severe, near-duplicate info). Decision: DROP sqft_above_log at Stage 6, keep sqft_living_log. Moderate VIF (6-7) on sqft_lot/sqft_lot15/sqft_basement — kept as-is.
- [x] Outlier strategy — DECISION: No winsorizing. Log-transform already compresses extreme values sufficiently; tree-based models (primary approach) are robust to remaining outliers; winsorizing risked destroying genuine luxury-property signal.
- [x] Scaler choice — DECISION: RobustScaler (uses median/IQR, not mean/std). Chosen specifically because we kept genuine outliers unwinsorized in Decision #3 — RobustScaler won't let luxury-property extremes distort scaling for the majority of "normal" houses.
- [x] lat/long — DECISION: KEEP raw lat/long in model input, alongside distance/cluster/PCA features. Reasoning: distance-based features are direction-blind (can't distinguish north-of-center from south-of-center); raw coordinates preserve that nuance. Tree-based models tolerate the redundancy well.
- [x] Confirmed grade/condition/view stay ordinal (numeric, no encoding). Reasoning: genuine order exists (higher = better), and King County's raw data already encodes them as ordered integers — one-hot encoding would destroy that ordering information the model can otherwise use directly.
- [x] Zipcode encoding — DECISION: Target encoding (map each zipcode to its average log_price). Reasoning: zipcode captures administrative/socioeconomic signal (school districts, zoning) distinct from pure geometric features (location_cluster, lat/long); one-hot would add 70+ sparse columns for modest gain. MUST be computed using X_train/y_train only, post-split, then mapped onto X_test — implemented in Stage 6/7.

## Stage 6 — Data Splitting ✅ CLOSED
- [x] 80/20 train/test split (17290 / 4323 rows)
- [x] Zipcode target encoding (leakage-safe, 0 missing in test)
- [x] Cluster average price encoding (leakage-safe, 0 missing in test)
- [x] Raw zipcode column dropped (fully represented by zipcode_encoded)
- [x] location_cluster kept as categorical feature (low cardinality, tree-model friendly)


## Stage 7 — Build the Pipeline ✅ CLOSED
- [x] ColumnTransformer built (numeric → RobustScaler, binary → passthrough, location_cluster → OneHotEncoder)
- [x] build_preprocessor() added to src/preprocess.py
- [x] Verified leakage-safe: fit_transform on X_train only, transform on X_test
- [x] Full pipeline confirmed reproducible end-to-end from src/ (17290,60) / (4323,60)

## Stage 8 — Baseline Model ✅ CLOSED
- [x] Dumb baseline (predict mean log_price) established
- [x] Baseline RMSE (log scale): 0.5340
- [x] Baseline MAE (log scale): 0.4187
- [x] Baseline R²: ~0.0000 (as expected — confirms calculation correctness)
- [x] Baseline MAE in real dollars: ~$229,795 — the floor every real model must beat

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

## Stage 16 (Preview) — Frontend UI ✅ SCAFFOLDED
- [x] Multi-page Streamlit app (Home, Predict, Market Explorer, Model Insights, About)
- [x] Custom theme (Pacific Northwest palette, Fraunces + Inter typography)
- [x] Custom sidebar (logo, nav, how-to-use, no default Streamlit nav)
- [x] KPI cards, welcome boxes, skeleton loading states
- [x] FastAPI backend scaffold with placeholder /predict endpoint
- [ ] NOTE: Predict/Model Insights pages use placeholder logic — real model wiring happens at Stage 15

## Stage 17 — Deployment
- [ ] Deploy backend + frontend (Render/Railway/HF Spaces)

## Stage 18 — Documentation & Polish
- [ ] `reports/feature_dictionary.md` — every feature explained
- [ ] Final README polish with visuals + live demo link
- [ ] Model report (`reports/model_report.md`)

---

## Git checkpoint convention
Commit + push at the end of every numbered stage above. No exceptions.