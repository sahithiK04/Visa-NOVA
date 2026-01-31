
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="VISA-NOVA API")

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    merchant: str
    country: str

@app.post("/analyze")
def analyze_transaction(txn: Transaction):
    return {
        "transaction_id": txn.transaction_id,
        "anomaly_score": 0.12,
        "risk_level": "LOW",
        "insight": "Transaction appears normal with low fraud risk."
    }
