"""Flask web UI: shows a form and calls the FastAPI service.  Run from project root:
    python web/app.py        ->  http://127.0.0.1:5000
"""
import os

import requests
from flask import Flask, render_template, request

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

app = Flask(__name__)

YN = ["Yes", "No"]
YNI = ["Yes", "No", "No internet service"]

CHOICES = {
    "gender": ["Female", "Male"],
    "SeniorCitizen": [("0", "No"), ("1", "Yes")],
    "Partner": YN,
    "Dependents": YN,
    "PhoneService": YN,
    "MultipleLines": ["Yes", "No", "No phone service"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "OnlineSecurity": YNI,
    "OnlineBackup": YNI,
    "DeviceProtection": YNI,
    "TechSupport": YNI,
    "StreamingTV": YNI,
    "StreamingMovies": YNI,
    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": YN,
    "PaymentMethod": ["Electronic check", "Mailed check",
                      "Bank transfer (automatic)", "Credit card (automatic)"],
}
NUMERIC = ["tenure", "MonthlyCharges", "TotalCharges"]


@app.route("/", methods=["GET", "POST"])
def index():
    result, error, form = None, None, {}
    if request.method == "POST":
        form = request.form.to_dict()
        try:
            payload = dict(form)
            payload["SeniorCitizen"] = int(payload["SeniorCitizen"])
            payload["tenure"] = int(payload["tenure"])
            payload["MonthlyCharges"] = float(payload["MonthlyCharges"])
            payload["TotalCharges"] = float(payload["TotalCharges"])

            r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            if r.ok:
                result = r.json()
                result["percent"] = round(result["churn_probability"] * 100, 1)
            else:
                error = f"API error {r.status_code}: {r.text}"
        except ValueError:
            error = "Please enter valid numbers for tenure and charges."
        except requests.exceptions.RequestException:
            error = f"Cannot reach the API at {API_URL}. Is the FastAPI server running?"
    return render_template("index.html", choices=CHOICES, numeric=NUMERIC,
                           result=result, error=error, form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
