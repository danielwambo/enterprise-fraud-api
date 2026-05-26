cat << 'EOF' > app/main.py
import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from app.schemas import TransactionInput, PredictionOutput

app = FastAPI(
    title="Enterprise Fraud Detection API",
    description="Production-grade Machine Learning API for real-time financial transaction scoring.",
    version="1.0.0"
)

MODEL = None

@app.on_event("startup")
def load_model():
    global MODEL
    # Dynamically find the absolute path of the root directory file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, "artifacts", "fraud_model.pkl")
    
    try:
        with open(model_path, "rb") as f:
            MODEL = pickle.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Model artifact not found at {model_path}. Please run the training script first.")

@app.get("/health", status_code=200)
def health_check():
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionOutput, status_code=200)
def predict_fraud(payload: TransactionInput):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model tracking matrix initialization failed.")
    
    features = np.array([[
        payload.amount,
        payload.old_balance,
        payload.new_balance,
        payload.is_merchant
    ]])
    
    prediction = int(MODEL.predict(features)[0])
    probability = float(MODEL.predict_proba(features)[0][1])
    
    return {
        "is_fraud": prediction,
        "fraud_probability": round(probability, 4)
    }
EOF
