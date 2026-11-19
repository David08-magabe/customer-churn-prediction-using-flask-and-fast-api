"""FastAPI service: serves the churn model.  Run from the project root:
    uvicorn api.main:app --reload --port 8000
Docs: http://127.0.0.1:8000/docs
"""
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from predictor import make_prediction

YesNo = Literal["Yes", "No"]
YesNoNoInternet = Literal["Yes", "No", "No internet service"]


class Customer(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0, 1]
    Partner: YesNo
    Dependents: YesNo
    tenure: int = Field(ge=0, le=100, description="Months with the company")
    PhoneService: YesNo
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: YesNoNoInternet
    OnlineBackup: YesNoNoInternet
    DeviceProtection: YesNoNoInternet
    TechSupport: YesNoNoInternet
    StreamingTV: YesNoNoInternet
    StreamingMovies: YesNoNoInternet
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: YesNo
    PaymentMethod: Literal[
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
    ]
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


class Prediction(BaseModel):
    prediction: Literal["Churn", "No Churn"]
    churn_probability: float


app = FastAPI(title="Customer Churn Prediction API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(customer: Customer):
    try:
        return make_prediction(customer.model_dump())
    except Exception as exc:  # e.g. unseen category, corrupt pickle
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")
