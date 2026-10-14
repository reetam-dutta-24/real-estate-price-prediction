# Model Report — King County Home Value

## Objective
Predict residential sale prices in King County, WA using structural, temporal, and geospatial features derived from 21,613 real 2014–2015 sales records.

## Approach Summary
1. EDA identified right-skewed price, geospatial price clustering, and a non-obvious age/renovation interaction
2. 100+ features engineered across temporal, structural, luxury, geospatial, and interaction categories
3. Leakage-safe preprocessing: skew correction, VIF-driven multicollinearity resolution, target encoding computed strictly post-split
4. Three algorithms compared via 5-fold cross-validation; XGBoost selected
5. Hyperparameters tuned via RandomizedSearchCV (30 candidates × 5-fold = 150 fits)
6. Final model interpreted via SHAP; performance validated via residual analysis

## Model Comparison

| Model | CV RMSE (log) | Test MAE ($) | Test R² |
|---|---|---|---|
| Baseline (mean) | 0.5340 | $229,795 | ~0.00 |
| Linear Regression | 0.1757 | $75,884 | 0.87 |
| Random Forest | 0.1710 | $68,481 | 0.89 |
| XGBoost (default) | 0.1663 | $66,631 | 0.90 |
| **XGBoost (tuned)** | **0.1558** (test) | **$62,141** | **0.9148** |

## Final Hyperparameters
n_estimators: 500
max_depth: 7
learning_rate: 0.05
subsample: 0.8
colsample_bytree: 0.7


## Key Findings
- **Zipcode encoding, luxury signals, and the grade×sqft_living interaction dominate feature importance** — confirms engineered features carry more signal than raw columns alone
- **The model performs strongly on mainstream housing (<$1M)** but shows reduced precision on luxury properties — residual analysis shows a funnel pattern with error growing at higher price points, consistent with sparser representation and higher price variance in that segment
- **House age alone showed no clear price trend in EDA**, but the trained model attributes renovation effects to `was_renovated`/`years_since_renovation` directly rather than through `house_age` — SHAP confirms the model learned this distinction correctly
- Linear Regression's meaningfully weaker performance (R² 0.87 vs. 0.91) confirms genuine non-linear relationships and feature interactions exist in this data, which tree-based models capture natively

## Limitations
- Trained on 2014–2015 data only — does not reflect current King County market conditions
- Reduced accuracy on luxury/waterfront properties (sparse training examples, high price variance)
- `luxury_score` uses hand-chosen weights (domain reasoning, not statistically fit)
- Model has not been validated against post-2015 sales

## Reproducibility
Full pipeline reproducible via `src/preprocess.py` and `src/train.py`. Experiment history tracked in MLflow (`mlflow.db`, SQLite backend, 5 logged runs).


## Interpreting the Evaluation Metrics

The final tuned XGBoost model achieved a test RMSE of 0.1558 on the log-price scale, a test MAE of $62,141, and a test R² of 0.9148.

- **RMSE (log scale):** Measures the square root of the average squared prediction error on the transformed target. Squaring the errors makes larger residuals contribute more heavily to the metric.
- **MAE (dollars):** Measures the average absolute prediction error expressed in dollars, making the reported value easier to interpret in the original price domain.
- **R²:** Measures the proportion of variance in the test target explained by the model relative to a mean-prediction baseline.

These metrics describe different aspects of model performance and should be interpreted together. In particular, the log-scale RMSE and dollar-scale MAE use different scales and should not be compared numerically as though they measured the same quantity.


## Generalization Considerations

The reported test metrics describe performance on the held-out test data drawn from the project's historical dataset. They do not establish equivalent accuracy on properties sold in later years or in other real estate markets.

King County sale prices and property characteristics may change over time. The model's 2014–2015 training data therefore limits the conclusions that can be drawn about present-day valuations.

Evaluating generalization to newer sales would require an appropriate newer dataset and a separate evaluation. Until that evaluation is performed, current-market accuracy remains unverified.

