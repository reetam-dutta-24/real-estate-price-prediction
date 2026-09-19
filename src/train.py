import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor


def evaluate_predictions(y_true_log, y_pred_log, label=""):
    """
    Stage 10: Computes RMSE (log scale), R², and MAE in real dollars
    for any set of true/predicted log_price values.
    """
    rmse = np.sqrt(mean_squared_error(y_true_log, y_pred_log))
    r2 = r2_score(y_true_log, y_pred_log)

    y_true_dollar = np.expm1(y_true_log)
    y_pred_dollar = np.expm1(y_pred_log)
    mae_dollar = mean_absolute_error(y_true_dollar, y_pred_dollar)

    results = {'label': label, 'rmse_log': rmse, 'r2': r2, 'mae_dollar': mae_dollar}
    print(f"{label} — RMSE(log): {rmse:.4f} | R²: {r2:.4f} | MAE: ${mae_dollar:,.0f}")
    return results


def train_baseline(y_train, y_test):
    """
    Stage 8: Dumb baseline — predicts the mean training log_price for every house.
    Returns the evaluation dict, for comparison against real models.
    """
    baseline_pred = np.full_like(y_test, fill_value=y_train.mean())
    return evaluate_predictions(y_test, baseline_pred, label="Baseline (mean)")


def compare_models(X_train_processed, y_train, X_test_processed, y_test):
    """
    Stage 9: Trains Linear Regression, Random Forest, and XGBoost.
    Evaluates each on the test set. Returns the dict of fitted models
    and a DataFrame summarizing their results.
    """
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    }

    all_results = []
    for name, model in models.items():
        model.fit(X_train_processed, y_train)
        preds = model.predict(X_test_processed)
        all_results.append(evaluate_predictions(y_test, preds, label=name))

    return models, pd.DataFrame(all_results)


def tune_xgboost(X_train_processed, y_train, n_iter=30, cv=5):
    """
    Stage 11: RandomizedSearchCV over XGBoost hyperparameters.
    Fit only on training data — leakage-safe.
    Returns the fitted RandomizedSearchCV object (use .best_estimator_ for the final model).
    """
    param_distributions = {
        'n_estimators': [100, 200, 300, 500],
        'max_depth': [3, 4, 5, 6, 7],
        'learning_rate': [0.01, 0.03, 0.05, 0.1, 0.15],
        'subsample': [0.7, 0.8, 0.9, 1.0],
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
    }

    xgb_base = XGBRegressor(random_state=42, n_jobs=-1)

    random_search = RandomizedSearchCV(
        estimator=xgb_base,
        param_distributions=param_distributions,
        n_iter=n_iter,
        cv=cv,
        scoring='neg_root_mean_squared_error',
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    random_search.fit(X_train_processed, y_train)

    print("Best parameters:", random_search.best_params_)
    print("Best CV RMSE:", -random_search.best_score_)

    return random_search