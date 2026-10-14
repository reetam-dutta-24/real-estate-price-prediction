# King County Home Value Predictor

🔗 **Live demo:** [kc-home-value.streamlit.app](https://kc-home-value.streamlit.app)
🔗 **API docs:** [kc-house-price-api.onrender.com/docs](https://kc-house-price-api.onrender.com/docs)

> The backend runs on a free-tier server that sleeps after ~15 minutes of inactivity. The first prediction after idle may take 30–60 seconds to respond while it wakes up — subsequent requests are fast.

An end-to-end machine learning project predicting residential real estate prices in King County, Washington (Seattle metro area) — from raw data through feature engineering, leakage-safe preprocessing, model training, and a deployed, explainable prediction application.

## Project Overview

This project builds a regression pipeline to estimate King County home prices using 21,613 real sale records from 2014–2015. Beyond a standard regression exercise, the focus is on doing the full ML lifecycle properly: rigorous exploratory analysis, deliberate feature engineering (100+ derived columns), leakage-aware preprocessing decisions backed by statistical reasoning (VIF, skew analysis), a tuned and interpretable model, and a genuinely functional full-stack application — not a notebook that stops at `.fit()`.

## Live Application

A four-step guided form collects property details, sends them to a live FastAPI backend running the trained model, and returns a full valuation report: estimated price with a confidence range, a SHAP-based breakdown of what's driving the estimate, comparable nearby sales, neighborhood statistics, and a pinned map of nearby amenities

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


## Documentation Guide

The project documentation is organized into three supporting documents:

- **[Project Roadmap](PROJECT_ROADMAP.md)** — Stage-by-stage development progress, preprocessing decisions, model training, evaluation, deployment, and remaining tasks.
- **[Feature Dictionary](reports/feature_dictionary.md)** — Definitions of raw and engineered features, including temporal, structural, quality, and geospatial features.
- **[Model Report](reports/model_report.md)** — Model comparison, tuned XGBoost configuration, evaluation results, interpretation findings, and documented limitations.

Together, these documents explain the project from feature construction and leakage-safe preprocessing through model evaluation and deployment. The README provides the high-level overview and setup instructions, while the supporting documents contain the implementation rationale and technical details.



## Making a Prediction

The application uses a four-step guided form to collect the property details required for a valuation.

After the user submits the form, the Streamlit frontend sends the property information to the FastAPI backend. The backend applies the saved preprocessing pipeline and trained XGBoost model to generate a price estimate.

The results page presents the estimated property value alongside a confidence range, a SHAP-based explanation of the prediction, comparable nearby sales, neighborhood statistics, and a map of nearby amenities.

The backend may take 30–60 seconds to respond to the first request after a period of inactivity because the free-tier service needs to wake up. Subsequent requests are typically faster.


## Model Limitations

The model was trained on 21,613 King County home-sale records from 2014–2015. Its predictions therefore reflect historical market data and should not be interpreted as guaranteed estimates of current property values.

Evaluation also identified reduced precision for luxury and waterfront properties, where the training data contains fewer examples and prices exhibit greater variability. The model performs more consistently on mainstream properties below $1 million.

These limitations are important when interpreting a prediction. The estimated value is a model-generated estimate based on the available features, not a formal property appraisal or a guarantee of a property's sale price.


## Prerequisites

Before running the application locally, ensure that Python is installed and that the project dependencies can be installed using pip.

The project has separate backend and frontend components, each with its own dependency requirements. The backend uses FastAPI to serve predictions, while the frontend uses Streamlit to provide the interactive application.

The trained model and preprocessing artifacts are required for inference. The original dataset is also needed when reproducing the data preparation and model training workflow from scratch.


## Understanding Prediction Results

The valuation report combines a predicted property value with supporting context to help users interpret the estimate.

The SHAP-based explanation identifies how individual input features influence the model's prediction. Comparable nearby sales and neighborhood statistics provide additional local context, while the amenities map visualizes nearby points of interest.

These elements serve different purposes: the model generates the estimate, SHAP explains feature contributions, and the additional geographic information helps users explore the surrounding area.


### Why XGBoost Was Selected

The project compared Linear Regression, Random Forest, and XGBoost rather than relying on a single algorithm from the beginning.

Linear Regression provides a baseline for understanding how far a linear model can go with the engineered features. Random Forest introduces an ensemble of decision trees, while XGBoost provides a gradient-boosted tree approach.

The tuned XGBoost model was selected because it achieved the strongest reported test performance among the compared models. Its selection was based on measured results rather than algorithm popularity alone.



### Reproducing the Machine Learning Workflow

The project separates exploratory analysis, preprocessing, model training, and application serving into distinct components.

The notebooks document the exploratory and experimental stages. The `src/` directory contains reusable preprocessing and training code, while the serialized artifacts in `models/` support prediction through the backend.

The frontend and backend can be run as separate services. Reproducing training and running the deployed-style prediction application are related but different workflows: training requires the dataset and model-building dependencies, whereas inference relies on the fitted artifacts and the prediction API.



## API Usage Example

The FastAPI service exposes interactive API documentation at `/docs`, where available endpoints and their request and response schemas can be explored.

A typical API-based prediction workflow is:

1. Prepare the property features required by the prediction endpoint.
2. Submit the request to the running backend.
3. Receive the estimated property value in the response.
4. Inspect the returned result alongside the application's explanation and comparison features, where available.

For the deployed service, visit the [API documentation](https://kc-house-price-api.onrender.com/docs).

**Note:** The exact request fields and response structure are defined by the API implementation. Use the live schema rather than assuming that every raw dataset column is accepted directly.


## Privacy and Input Handling

Property valuation inputs should be limited to the information needed to generate an estimate.

- Submit property attributes through the application's intended input interface.
- Avoid including personal or confidential information in free-text fields or diagnostic reports.
- Treat model predictions as estimates rather than verified property valuations.
- Review the application's data-handling practices before submitting sensitive information.

The prediction describes an estimate produced by a machine learning model; it is not a substitute for a professional appraisal or an independent assessment of a property's current market value.


## Project Architecture

The project separates the user-facing application from the machine learning inference service.

- **Frontend:** Provides the interface for entering property details and viewing valuation results.
- **Backend API:** Handles prediction requests and exposes endpoints through FastAPI.
- **Machine learning layer:** Uses the trained model and the expected feature representation to generate estimates.
- **Explanation layer:** Supports interpretation of predictions through feature contributions and property comparisons where implemented.
- **Deployment:** The frontend and backend are hosted separately, so the frontend must communicate with the correct backend URL.

This separation makes it easier to develop, deploy, and troubleshoot individual application components.


## Understanding Model Limitations

A predicted property value is an estimate based on patterns learned from historical transaction data.

Prediction quality can be affected by:

- Market conditions that differ from the training period.
- Unusual properties with few comparable observations.
- Missing, inaccurate, or inconsistent input attributes.
- Differences between the training data and the property being evaluated.
- Factors that are not represented in the available features.

The reported test metrics summarize performance on a particular evaluation dataset. They do not guarantee the same accuracy for every property or in every market condition.