"""Loads the artifacts saved by the notebook and exposes make_prediction()."""
import os
import pickle
from pathlib import Path

import pandas as pd

MODELS_DIR = Path(os.getenv("MODELS_DIR", Path(__file__).resolve().parent / "models"))

# Same column order the model was trained on (customerID dropped, Churn is the target)
FEATURE_ORDER = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges",
]
NUMERICAL_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]


def _load(name: str):
    with open(MODELS_DIR / name, "rb") as f:
        return pickle.load(f)


model = _load("best_model.pkl")
encoders = _load("encoder.pkl")
scaler = _load("scaler.pkl")


def make_prediction(data: dict) -> dict:
    df = pd.DataFrame([data])[FEATURE_ORDER]
    for col, encoder in encoders.items():
        df[col] = encoder.transform(df[col])
    df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS])

    pred = int(model.predict(df)[0])
    prob = float(model.predict_proba(df)[0, 1])
    return {
        "prediction": "Churn" if pred == 1 else "No Churn",
        "churn_probability": round(prob, 4),
    }
