import pandas as pd
import numpy as np
from scipy.stats import skew
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def load_data(path="data/raw/kc_house_data.csv"):
    """Load the raw King County housing dataset."""
    df = pd.read_csv(path)
    return df


def clean_data(df):
    """Stage 2: Data Cleaning."""
    df = df.drop(columns=['Unnamed: 0', 'id'], errors='ignore')

    df['date'] = pd.to_datetime(df['date'])
    df['sale_year'] = df['date'].dt.year
    df['sale_month'] = df['date'].dt.month

    df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
    df['bathrooms'] = df['bathrooms'].fillna(df['bathrooms'].median())

    # Known data-entry error: 33 bedrooms -> 3
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


def engineer_core_features(df):
    """Original core features: age, renovation, basement, distance, ratios, log_price."""
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


def engineer_temporal_features(df):
    """Category 1: Temporal features."""
    df['sale_quarter'] = df['date'].dt.quarter
    df['sale_day_of_week'] = df['date'].dt.dayofweek
    df['is_peak_season'] = df['sale_month'].isin([5, 6, 7, 8]).astype(int)
    df['decade_built'] = (df['yr_built'] // 10) * 10
    df['renovation_decade'] = np.where(
        df['yr_renovated'] > 0,
        (df['yr_renovated'] // 10) * 10,
        0
    )
    df['sale_month_sin'] = np.sin(2 * np.pi * df['sale_month'] / 12)
    df['sale_month_cos'] = np.cos(2 * np.pi * df['sale_month'] / 12)
    return df


def engineer_size_features(df):
    """Category 2: Size & structure ratios."""
    df['above_ratio'] = df['sqft_above'] / df['sqft_living']
    df['living_sqft_diff_from_neighbors'] = df['sqft_living'] - df['sqft_living15']
    df['lot_sqft_diff_from_neighbors'] = df['sqft_lot'] - df['sqft_lot15']
    df['total_rooms_estimate'] = df['bedrooms'] + df['bathrooms']
    return df


def engineer_luxury_features(df):
    """Category 3: Quality / luxury signals."""
    df['view_binary'] = (df['view'] > 0).astype(int)
    df['is_luxury'] = ((df['waterfront'] == 1) | (df['grade'] >= 11) | (df['view'] >= 3)).astype(int)
    df['luxury_score'] = (
        df['grade'] * 1.0 +
        df['view'] * 2.0 +
        df['waterfront'] * 5.0 +
        df['condition'] * 0.5
    )
    return df


def engineer_geospatial_features(df, n_clusters=15):
    """Category 4: Geospatial — Bellevue distance, KMeans clusters, 50 landmarks + PCA."""
    bellevue_lat, bellevue_lon = 47.6101, -122.2015
    df['distance_to_bellevue'] = haversine_distance(df['lat'], df['long'], bellevue_lat, bellevue_lon)

    # KMeans location clusters (lat/long only — leakage-safe, no price involved)
    coords = df[['lat', 'long']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['location_cluster'] = kmeans.fit_predict(coords)

    # 50 landmark distances
    landmarks = {
        'seatac_airport': (47.4502, -122.3088),
        'boeing_field': (47.5301, -122.3018),
        'university_of_washington_station': (47.6497, -122.3039),
        'amazon_hq_seattle': (47.6221, -122.3365),
        'microsoft_redmond': (47.6396, -122.1281),
        'boeing_everett': (47.9142, -122.2777),
        'google_kirkland': (47.6769, -122.1959),
        'expedia_seattle': (47.6156, -122.3861),
        'university_of_washington': (47.6553, -122.3035),
        'seattle_university': (47.6086, -122.3138),
        'bellevue_college': (47.5786, -122.1500),
        'harborview_medical_center': (47.6041, -122.3238),
        'uw_medical_center': (47.6493, -122.3084),
        'seattle_childrens_hospital': (47.6626, -122.2820),
        'overlake_medical_center': (47.6157, -122.1875),
        'evergreen_health_medical_center': (47.7012, -122.2029),
        'pike_place_market': (47.6097, -122.3422),
        'downtown_bellevue': (47.6101, -122.2015),
        'downtown_kirkland': (47.6769, -122.2059),
        'downtown_redmond': (47.6740, -122.1215),
        'downtown_renton': (47.4829, -122.2171),
        'downtown_kent': (47.3809, -122.2348),
        'downtown_auburn': (47.3073, -122.2285),
        'downtown_issaquah': (47.5301, -122.0326),
        'bellevue_square': (47.6161, -122.2042),
        'westfield_southcenter': (47.4589, -122.2586),
        'alderwood_mall': (47.8399, -122.2761),
        'discovery_park': (47.6613, -122.4152),
        'woodland_park_zoo': (47.6685, -122.3541),
        'alki_beach': (47.5813, -122.4098),
        'lake_sammamish': (47.6003, -122.0426),
        'lake_washington_kirkland': (47.6769, -122.2059),
        'cougar_mountain': (47.5301, -122.1215),
        'mercer_slough_nature_park': (47.5893, -122.2093),
        'gene_coulon_park': (47.5031, -122.2001),
        'space_needle': (47.6205, -122.3493),
        'seattle_art_museum': (47.6075, -122.3382),
        'climate_pledge_arena': (47.6221, -122.3540),
        'lumen_field': (47.5952, -122.3316),
        't_mobile_park': (47.5914, -122.3325),
        'chihuly_garden_and_glass': (47.6209, -122.3505),
        'downtown_shoreline': (47.7557, -122.3419),
        'downtown_federal_way': (47.3223, -122.3126),
        'downtown_burien': (47.4704, -122.3468),
        'mercer_island_town_center': (47.5707, -122.2221),
        'downtown_tukwila': (47.4740, -122.2610),
        'sammamish_town_center': (47.6163, -122.0356),
        'newcastle_wa': (47.5352, -122.1637),
        'north_bend_wa': (47.4931, -121.7869),
        'vashon_island': (47.4459, -122.4638),
        'snoqualmie_falls': (47.5417, -121.8375),
    }

    for name, (lat, lon) in landmarks.items():
        df[f'distance_to_{name}'] = haversine_distance(df['lat'], df['long'], lat, lon)

    # PCA compression of the 50 landmark distances
    distance_cols = [c for c in df.columns if c.startswith('distance_to_')
                      and c not in ['distance_to_seattle', 'distance_to_bellevue']]

    scaler = StandardScaler()
    distance_scaled = scaler.fit_transform(df[distance_cols])

    pca = PCA(n_components=3, random_state=42)
    distance_pca = pca.fit_transform(distance_scaled)

    df['amenity_proximity_pc1'] = distance_pca[:, 0]
    df['amenity_proximity_pc2'] = distance_pca[:, 1]
    df['amenity_proximity_pc3'] = distance_pca[:, 2]

    return df


def engineer_interaction_features(df):
    """Category 5: Interaction features."""
    df['grade_x_sqft_living'] = df['grade'] * df['sqft_living']
    df['age_x_renovated'] = df['house_age'] * df['was_renovated']
    return df


def apply_log_transforms(df):
    """Stage 5: log-transform skewed sqft columns."""
    skewed_cols = ['sqft_lot', 'sqft_lot15', 'sqft_basement',
                   'sqft_living', 'sqft_above', 'sqft_living15']
    for col in skewed_cols:
        df[f'{col}_log'] = np.log1p(df[col])
    return df


def add_city_names(df):
    """Display-only: zipcode -> city name via pgeocode."""
    import pgeocode
    nomi = pgeocode.Nominatim('us')
    unique_zips = df['zipcode'].astype(str).unique()
    zip_lookup = nomi.query_postal_code(unique_zips)
    zip_to_city = dict(zip(zip_lookup['postal_code'].astype(str), zip_lookup['place_name']))
    df['city_name'] = df['zipcode'].astype(str).map(zip_to_city)
    return df


def engineer_features(df):
    """Runs ALL feature engineering steps in the correct order."""
    df = engineer_core_features(df)
    df = engineer_temporal_features(df)
    df = engineer_size_features(df)
    df = engineer_luxury_features(df)
    df = engineer_geospatial_features(df)
    df = engineer_interaction_features(df)
    df = apply_log_transforms(df)
    df = add_city_names(df)
    return df


def split_data(df, target='log_price', test_size=0.2, random_state=42):
    """Stage 6: 80/20 train/test split. Drops leakage/display/redundant columns."""
    drop_cols = [
        'price', 'log_price', 'date', 'city_name', 'sqft_above_log',
        'sqft_living', 'sqft_lot', 'sqft_above', 'sqft_basement',
        'sqft_living15', 'sqft_lot15',
    ]
    distance_cols = [c for c in df.columns if c.startswith('distance_to_')]
    drop_cols += distance_cols

    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test