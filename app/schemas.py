from pydantic import BaseModel, Field

class TransactionInput(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount in USD/KES", example=2500.50)
    old_balance: float = Field(..., ge=0, description="Balance before transaction", example=5000.00)
    new_balance: float = Field(..., ge=0, description="Balance after transaction", example=2499.50)
    is_merchant: int = Field(..., ge=0, le=1, description="1 if destination is merchant, 0 otherwise", example=0)

class PredictionOutput(BaseModel):
    is_fraud: int = Field(..., description="1 for fraudulent, 0 for legitimate")
    fraud_probability: float = Field(..., description="Probability score between 0 and 1")
