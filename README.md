<img width="1536" height="1024" alt="Electricity bill prediction system flow" src="https://github.com/user-attachments/assets/03ef189c-7a03-4d1d-ad22-5a05e86483e8" /># ⚡ Electricity Bill Predictor

A **Python-based ML project** that predicts electricity bills and provides cost-saving suggestions. Built with **FastAPI** backend and **Streamlit** frontend, it supports **daily, weekly, and monthly predictions** and visualizes potential savings.

## 🚀 Features
- Predict electricity bills for **daily, weekly, and monthly usage**
- Cost-saving suggestions based on energy consumption
- Estimated bill after applying suggested savings
- Clean and interactive **Streamlit UI**
- Scalable backend using **FastAPI** and **pickle ML model**

## 🧠 Tech Stack
- Scikit-learn
- FastAPI
- Streamlit
- Python

## 📊 Dataset
Household Power Consumption Dataset

## Architecture

![Project Architecture]
<img width="1536" height="1024" alt="Electricity bill prediction system flow" src="https://github.com/user-attachments/assets/02542551-40d5-4fa5-ae12-54989081b9cd" />


- **Frontend**: Streamlit app (`frontend/ui.py`)
- **Backend**: FastAPI (`backend/app.py`) serving predictions
- **Model**: Scikit-learn regression model (`model/model.pkl`)
  
## ▶️ Run Project
1. Train model:
   python train_model.py

2. Start API:
   cd backend
   uvicorn app:app --reload

3. Run UI:
   cd frontend
   streamlit run ui.py
