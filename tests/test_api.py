from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Asserts the application boots up and loads the ML model properly."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model_loaded": True}

def test_predict_legitimate_transaction():
    """Asserts low-amount standard transactions are flagged as safe."""
    payload = {
        "amount": 20.0,
        "old_balance": 10.0,
        "new_balance": 30.0,
        "is_merchant": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_fraud" in data
    assert "fraud_probability" in data
    assert data["is_fraud"] == 0

def test_predict_fraudulent_transaction():
    """Asserts high-volume anomaly transactions register high fraud risk."""
    payload = {
        "amount": 120000.0,
        "old_balance": 150000.0,
        "new_balance": 30000.0,
        "is_merchant": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_fraud"] == 1

def test_invalid_payload_validation():
    """Asserts the API rejects bad formats (e.g. negative transactions)."""
    payload = {
        "amount": -500.0,  # Invalid: must be greater than 0
        "old_balance": 100.0,
        "new_balance": 50.0,
        "is_merchant": 3   # Invalid: must be 0 or 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
