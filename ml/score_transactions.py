import os
import joblib
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ======================================================
# LOAD ENV VARIABLES
# ======================================================
load_dotenv()

# ======================================================
# PATH SETUP
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "isolation_forest.pkl"
SCALER_PATH = BASE_DIR / "ml" / "scaler.pkl"

# ======================================================
# LOAD MODEL & SCALER
# ======================================================
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ======================================================
# SQLALCHEMY DATABASE ENGINE
# ======================================================
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ======================================================
# LOAD TRANSACTIONS
# ======================================================
query = """
SELECT
    id,
    time_seconds,
    amount,
    v1, v2, v3, v4, v5, v6, v7,
    v8, v9, v10, v11, v12, v13, v14,
    v15, v16, v17, v18, v19, v20,
    v21, v22, v23, v24, v25, v26,
    v27, v28
FROM transactions
"""

df = pd.read_sql(query, engine)

ids = df["id"]
features = df.drop(columns=["id"])

# ======================================================
# RENAME COLUMNS (MATCH TRAINING DATA)
# ======================================================
features = features.rename(columns={
    "time_seconds": "Time",
    "amount": "Amount",
    **{f"v{i}": f"V{i}" for i in range(1, 29)}
})

# ======================================================
# FORCE FEATURE ORDER
# ======================================================
FEATURE_ORDER = (
    ["Time"] +
    [f"V{i}" for i in range(1, 29)] +
    ["Amount"]
)

features = features[FEATURE_ORDER]

# ======================================================
# SCALE FEATURES
# ======================================================
X_scaled = scaler.transform(features)

# ======================================================
# ANOMALY SCORING
# ======================================================
raw_scores = -model.decision_function(X_scaled)

norm_scaler = MinMaxScaler()
anomaly_scores = norm_scaler.fit_transform(
    raw_scores.reshape(-1, 1)
).flatten()

# ======================================================
# ASSIGN RISK LEVELS
# ======================================================
def risk_from_score(score: float) -> str:
    if score >= 0.75:
        return "HIGH"
    elif score >= 0.40:
        return "MEDIUM"
    else:
        return "LOW"

risk_levels = [risk_from_score(score) for score in anomaly_scores]

# ======================================================
# UPDATE DATABASE (SQLALCHEMY 2.x SAFE)
# ======================================================
update_stmt = text("""
    UPDATE transactions
    SET anomaly_score = :anomaly_score,
        risk_level = :risk_level
    WHERE id = :id
""")

with engine.begin() as conn:
    for i in range(len(ids)):
        conn.execute(
            update_stmt,
            {
                "anomaly_score": float(anomaly_scores[i]),
                "risk_level": risk_levels[i],
                "id": int(ids.iloc[i])
            }
        )

print("✅ Transactions scored and database updated successfully")
