import os
import pickle
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

def train():
    print("Generating synthetic financial transaction data...")
    # Creating dummy fraud data (Amount, OldBalance, NewBalance, IsMerchant)
    data = {
        'amount': [100.0, 50000.0, 20.0, 90000.0, 150.0, 120000.0] * 100,
        'old_balance': [200.0, 60000.0, 10.0, 100000.0, 500.0, 150000.0] * 100,
        'new_balance': [100.0, 10000.0, 30.0, 10000.0, 350.0, 30000.0] * 100,
        'is_merchant': [0, 0, 1, 0, 1, 0] * 100,
        'is_fraud': [0, 1, 0, 1, 0, 1] * 100
    }
    df = pd.DataFrame(data)
    
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost Production Model...")
    model = XGBClassifier(n_estimators=50, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    os.makedirs('artifacts', exist_ok=True)
    with open('artifacts/fraud_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model successfully saved to artifacts/fraud_model.pkl")

if __name__ == "__main__":
    train()
