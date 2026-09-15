import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def load_data(path="data/raw/kc_house_data.csv"):
    """Load the raw King County housing dataset."""
    df = pd.read_csv(path)
    return df


def clean_data(df):
    """Apply Stage 2 cleaning steps."""
    df = df.drop(columns=['Unnamed: 0', 'id'], errors='ignore')

    df['date'] = pd.to_datetime(df['date'])
    df['sale_year'] = df['date'].dt.year
    df['sale_month'] = df['date'].dt.month

    df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
    df['bathrooms'] = df['bathrooms'].fillna(df['bathrooms'].median())

    # Fix known data-entry error: 33 bedrooms -> 3
    df.loc[df['bedrooms'] == 33, 'bedrooms'] = 3

    return df


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def engineer_features(df):
    """Apply Stage 3 feature engineering steps."""
    df['house_age'] = df['sale_year'] - df['yr_built']

    df['was_renovated'] = (df['yr_renovated'] > 0).astype(int)
    df['years_since_renovation'] = df.apply(
        lambda row: row['sale_year'] - row['yr_renovated'] if row['yr_renovated'] > 0 else row['house_age'],
        axis=1
    )

    df['has_basement'] = (df['sqft_basement'] > 0).astype(int)

    seattle_lat, seattle_lon = 47.6062, -122.3321
    df['distance_to_seattle'] = haversine_distance(df['lat'], df['long'], seattle_lat, seattle_lon)

    df['sqft_ratio'] = df['sqft_living'] / df['sqft_lot']
    df['bed_bath_ratio'] = df['bedrooms'] / df['bathrooms'].replace(0, 1)

    df['log_price'] = np.log1p(df['price'])

    return df

def split_data(df, target='log_price', test_size=0.2, random_state=42):
    """Split into train/test sets. Drops raw price/date columns from features."""
    drop_cols = ['price', 'log_price', 'date']
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


