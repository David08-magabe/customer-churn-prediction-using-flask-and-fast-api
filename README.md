# Customer Churn Prediction App

- **FastAPI** (`api/main.py`) – serves the model at `POST /predict`
- **Flask** (`web/app.py`) – web form that calls the FastAPI service
- `predictor.py` – loads the pickles from your notebook and runs the same preprocessing

## 1. Add the model files
Run your notebook once and copy these 3 files into `models/`:
`best_model.pkl`, `encoder.pkl`, `scaler.pkl`

Use the same scikit-learn version for the app as in the notebook
(`pip freeze | grep scikit-learn` in the notebook environment) or the pickles may fail to load.

## 2. Install
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt

## 3. Run (two terminals, from the project root)
    uvicorn api.main:app --reload --port 8000
    python web/app.py

- Web UI:  http://127.0.0.1:5000
- API docs: http://127.0.0.1:8000/docs

## Test the API directly
    curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{
      "gender":"Female","SeniorCitizen":0,"Partner":"Yes","Dependents":"No","tenure":1,
      "PhoneService":"No","MultipleLines":"No phone service","InternetService":"DSL",
      "OnlineSecurity":"No","OnlineBackup":"Yes","DeviceProtection":"No","TechSupport":"No",
      "StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month",
      "PaperlessBilling":"Yes","PaymentMethod":"Electronic check",
      "MonthlyCharges":29.85,"TotalCharges":29.85}'
