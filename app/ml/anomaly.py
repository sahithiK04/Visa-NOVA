import numpy as np
from sklearn.ensemble import IsolationForest
from app.db import get_db

def run_anomaly_detection():
    conn = get_db()
    cur = conn.cursor()

    # Fetch features
    cur.execute("""
        SELECT
            id,
            time_seconds,
            amount,
            v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,
            v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,
            v21,v22,v23,v24,v25,v26,v27,v28
        FROM transactions
    """)

    rows = cur.fetchall()

    ids = []
    features = []

    for row in rows:
        ids.append(row[0])
        features.append(list(row[1:]))

    X = np.array(features)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.03,   # ~3% anomalies
        random_state=42
    )

    model.fit(X)

    scores = model.decision_function(X)   # higher = more normal
    anomaly_scores = -scores              # higher = more anomalous

    # Normalize to 0–1
    min_s, max_s = anomaly_scores.min(), anomaly_scores.max()
    normalized = (anomaly_scores - min_s) / (max_s - min_s)

    # Update DB
    for txn_id, score in zip(ids, normalized):
        if score > 0.95:
            risk = "HIGH"
        elif score > 0.85:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        cur.execute(
            """
            UPDATE transactions
            SET anomaly_score = %s,
                risk_level = %s
            WHERE id = %s
            """,
            (float(score), risk, txn_id)
        )

    conn.commit()
    cur.close()
    conn.close()

    return len(ids)
