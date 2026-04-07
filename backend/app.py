from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os

app = FastAPI()

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "model.pkl")
model = pickle.load(open(model_path, "rb"))

# Request model
class EnergyRequestPeriod(BaseModel):
    units: float
    period: str  # "daily", "weekly", "monthly"

# --- Add this route ---
@app.post("/predict_period")
def predict_bill_period(request: EnergyRequestPeriod):
    units = [[request.units]]
    predicted_bill = model.predict(units)[0]

    # Cost-saving suggestion
    if request.units < 30:
        suggestion = "✅ Usage is low, keep it up!"
    elif request.units < 60:
        suggestion = "⚡ Consider switching off unused appliances."
    elif request.units < 100:
        suggestion = "⚡ Reduce heavy appliance usage during peak hours."
    else:
        suggestion = "❌ High usage! Consider energy-efficient devices."

    return {
        "units": request.units,
        "period": request.period,
        "predicted_bill": round(predicted_bill, 2),
        "suggestion": suggestion
    }