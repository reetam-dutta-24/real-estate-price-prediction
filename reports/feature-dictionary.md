# Feature Dictionary

Every feature used in the King County Home Value model, what it means, and why it exists. Raw dataset columns are marked **(raw)**; everything else was engineered.

## Target
| Feature | Description |
|---|---|
| `log_price` | Log-transformed sale price (`log1p(price)`). Model trains on this, not raw `price`, to correct for right-skew. |

## Core Property Attributes (raw)
| Feature | Description |
|---|---|
| `bedrooms`, `bathrooms` | Room counts. One 33-bedroom entry corrected to 3 (data entry error). |
| `sqft_living`, `sqft_lot`, `sqft_above`, `sqft_basement` | Size measures (sqft). Log-transformed versions used in the model (see below); `sqft_above` dropped due to severe multicollinearity with `sqft_living_log` (VIF > 26). |
| `floors`, `waterfront`, `view`, `condition`, `grade` | Structural/quality ratings. `grade`/`condition`/`view` kept as ordinal numerics (not one-hot encoded — order is meaningful). |
| `yr_built`, `yr_renovated` | Construction/renovation year. |
| `lat`, `long` | Coordinates. Kept raw in the model alongside derived distance features — distance metrics are direction-blind, raw coordinates preserve that nuance. |
| `sqft_living15`, `sqft_lot15` | Living/lot size of the 15 nearest neighboring houses. |

## Log-Transformed Size Features
| Feature | Why |
|---|---|
| `sqft_living_log`, `sqft_lot_log`, `sqft_basement_log`, `sqft_living15_log`, `sqft_lot15_log` | Raw versions were significantly right-skewed (skew up to 13.06 for `sqft_lot`). Log-transform reduced skew to under 1.0 across all five. |

## Temporal Features
| Feature | Description |
|---|---|
| `sale_year`, `sale_month`, `sale_quarter`, `sale_day_of_week` | Extracted from the sale `date`. |
| `sale_month_sin`, `sale_month_cos` | Cyclical encoding of month — ensures December and January are numerically "close," which a raw 1–12 scale doesn't capture. |
| `is_peak_season` | Binary flag for May–August sales (historically strongest US real estate months). |
| `house_age` | `sale_year - yr_built`. |
| `decade_built`, `renovation_decade` | `yr_built`/`yr_renovated` bucketed into decades — captures architectural-era effects raw year misses. |
| `was_renovated` | Binary flag (`yr_renovated > 0`). |
| `years_since_renovation` | Years since renovation, or `house_age` if never renovated. |

## Size & Structure Ratios
| Feature | Description |
|---|---|
| `above_ratio` | `sqft_above / sqft_living` — proportion of living space above ground. |
| `living_sqft_diff_from_neighbors` | `sqft_living - sqft_living15` — is this house bigger/smaller than its immediate neighborhood? |
| `lot_sqft_diff_from_neighbors` | Same idea, for lot size. |
| `total_rooms_estimate` | `bedrooms + bathrooms`. |
| `sqft_ratio` | `sqft_living / sqft_lot`. |
| `bed_bath_ratio` | `bedrooms / bathrooms` (zero-bathroom guarded). |
| `has_basement` | Binary flag (`sqft_basement > 0`). |

## Quality / Luxury Signals
| Feature | Description |
|---|---|
| `view_binary` | Binary — any view at all (`view > 0`). |
| `is_luxury` | Composite flag: waterfront OR grade ≥ 11 OR view ≥ 3. ~5.7% of dataset flagged. |
| `luxury_score` | Hand-weighted composite (`grade*1.0 + view*2.0 + waterfront*5.0 + condition*0.5`). Weights chosen by domain reasoning, not statistically derived — documented explicitly as a heuristic feature. |

## Geospatial Features
| Feature | Description |
|---|---|
| `distance_to_seattle`, `distance_to_bellevue` | Haversine distance (km) to the two major King County job/urban hubs. |
| `location_cluster` | KMeans cluster ID (15 clusters), fit on `lat`/`long` only — no price used, leakage-safe. One-hot encoded in the final pipeline. |
| `cluster_avg_price` | Average `log_price` per `location_cluster`, computed **on training data only**, mapped onto test/inference data — leakage-safe target encoding. |
| `zipcode_encoded` | Average `log_price` per zipcode, same leakage-safe pattern. Replaces raw `zipcode` (dropped from the model). |
| `amenity_proximity_pc1/pc2/pc3` | PCA components (3, retaining 95%+ variance) compressed from 50 raw landmark-distance features (airports, employers, hospitals, parks, etc.) — avoids feeding 50 highly-correlated raw distances into the model. |
| `grade_x_sqft_living` | Interaction term — captures that large + high-grade compounds value disproportionately. |
| `age_x_renovated` | Interaction term — `house_age * was_renovated`. |

## Display-Only (Not in Model)
| Feature | Description |
|---|---|
| `city_name` | Zipcode → readable place name via `pgeocode`. Used only in the frontend UI, never fed to the model. |

## Explicitly Avoided
| Feature | Why not included |
|---|---|
| `price_per_sqft` | Would directly encode the target (`price`) into a feature — textbook data leakage. Never computed as a model input. |

## Final Model Input
**46 raw/engineered columns → 60 columns after preprocessing** (RobustScaler on numerics, passthrough on binary flags, one-hot encoding expands `location_cluster` from 1 column to 15).