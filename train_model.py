import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# 1. Load dataset
df = pd.read_csv("data/household_power_consumption.csv")

# 2. Normalize column names
df.columns = df.columns.str.strip().str.lower()

# 3. Clean data
df.replace('?', None, inplace=True)
df['global_active_power'] = pd.to_numeric(df['global_active_power'], errors='coerce')
df.dropna(inplace=True)

# 4. Create datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# 5. Convert power (kW) → energy per minute (kWh)
df['energy_kwh'] = df['global_active_power'] / 60

# 6. Aggregate daily energy
daily = df.groupby(df['datetime'].dt.date)['energy_kwh'].sum().reset_index()
daily.columns = ['date', 'daily_units']

# 7. Calculate electricity bill
def calculate_bill(units):
    if units <= 60:
        return units * 30
    elif units <= 120:
        return (60 * 30) + (units - 60) * 50
    else:
        return (60 * 30) + (60 * 50) + (units - 120) * 75

daily['bill'] = daily['daily_units'].apply(calculate_bill)

# 8. Train model
model = LinearRegression()
model.fit(daily[['daily_units']], daily['bill'])

# 9. Save model
import os
os.makedirs("backend/model", exist_ok=True)
pickle.dump(model, open("backend/model/model.pkl", "wb"))

print("✅ Model trained and saved successfully!")

class EnergyRequestPeriod(BaseModel):
    units: float  # Could be daily/weekly/monthly units
    period: str   # "daily", "weekly", "monthly"

@app.post("/predict_period")
def predict_bill_period(request: EnergyRequestPeriod):
    units = [[request.units]]
    predicted_bill = model.predict(units)[0]
    suggestion = suggest_savings(request.units)
    return {
        "units": request.units,
        "period": request.period,
        "predicted_bill": round(predicted_bill, 2),
        "suggestion": suggestion
    }

import matplotlib.pyplot as plt

# Example: Plot weekly usage
weekly_data = {'week': ['Week 1', 'Week 2', 'Week 3'], 'bill': [120, 150, 110]}
fig, ax = plt.subplots()
ax.bar(weekly_data['week'], weekly_data['bill'], color='skyblue')
ax.set_ylabel('Predicted Bill (Rs)')
ax.set_title('Weekly Electricity Bill')
st.pyplot(fig)