from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="House Price Prediction API")


class HouseFeatures(BaseModel):
    sqft_living: float
    bedrooms: int
    bathrooms: float
    grade: int
    lat: float
    long: float


@app.get("/")
def root():
    return {"message": "House Price Prediction API is running"}


@app.post("/predict")
def predict(features: HouseFeatures):
    # PLACEHOLDER — real model will replace this in Stage 15
    dummy_prediction = 500000
    return {"predicted_price": dummy_prediction, "note": "placeholder — real model not yet connected"}