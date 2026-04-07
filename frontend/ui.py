import streamlit as st
import requests

st.title("⚡ Smart Electricity Cost Analyzer")

# -----------------------
# Cost-saving logic
def estimate_savings(units):
    """
    Estimate potential kWh savings based on usage.
    """
    if units > 100:
        return round(units * 0.15, 2)  # suggest 15% reduction
    elif units > 60:
        return round(units * 0.10, 2)  # suggest 10% reduction
    else:
        return 0  # already low usage

# -----------------------
# User input
period = st.selectbox("Select period:", ["Daily", "Weekly", "Monthly"])
units = st.number_input(f"Enter your {period.lower()} electricity usage (kWh):", min_value=0.0, step=0.1)

# -----------------------
# Predict button
if st.button(f"Predict {period} Bill"):
    payload = {"units": units, "period": period.lower()}
    try:
        response = requests.post("http://127.0.0.1:8000/predict_period", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Show predicted bill and suggestion from API
        st.success(f"Predicted {period.lower()} bill: Rs. {data['predicted_bill']}")
        st.info(f"💡 Suggestion: {data['suggestion']}")

        # Show cost-saving dashboard
        potential_savings_units = estimate_savings(units)
        if potential_savings_units > 0:
            st.warning(f"💰 Potential savings: {potential_savings_units} kWh!")
            # Estimate new bill by reducing units and calling API again
            new_payload = {"units": units - potential_savings_units, "period": period.lower()}
            new_response = requests.post("http://127.0.0.1:8000/predict_period", json=new_payload, timeout=5)
            if new_response.status_code == 200:
                new_data = new_response.json()
                st.success(f"💸 Estimated bill after savings: Rs. {round(new_data['predicted_bill'],2)}")
        else:
            st.write("✅ Your usage is already low, keep it up!")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")