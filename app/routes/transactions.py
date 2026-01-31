from fastapi import APIRouter, Query
from app.db import get_db

router = APIRouter()

# =====================================================
# 1️⃣ GET TRANSACTIONS
# =====================================================
@router.get("/transactions")
def get_transactions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            time_seconds,
            amount,
            actual_fraud,
            anomaly_score,
            risk_level
        FROM transactions
        ORDER BY id
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "data": [
            {
                "id": r[0],
                "time_seconds": r[1],
                "amount": float(r[2]),
                "actual_fraud": r[3],
                "anomaly_score": r[4],
                "risk_level": r[5]
            }
            for r in rows
        ]
    }


# =====================================================
# 2️⃣ GET HIGH-RISK ANOMALIES
# =====================================================
@router.get("/transactions/anomalies")
def get_anomalies(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            amount,
            actual_fraud,
            anomaly_score,
            risk_level
        FROM transactions
        WHERE risk_level = 'HIGH'
        ORDER BY anomaly_score DESC
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "data": [
            {
                "id": r[0],
                "amount": float(r[1]),
                "actual_fraud": r[2],
                "anomaly_score": r[3],
                "risk_level": r[4]
            }
            for r in rows
        ]
    }


# =====================================================
# 3️⃣ GET TRANSACTION BY ID
# =====================================================
@router.get("/transactions/{transaction_id}")
def get_transaction_by_id(transaction_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            time_seconds,
            amount,
            actual_fraud,
            anomaly_score,
            risk_level
        FROM transactions
        WHERE id = %s
        """,
        (transaction_id,)
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {"message": "Transaction not found"}

    return {
        "id": row[0],
        "time_seconds": row[1],
        "amount": float(row[2]),
        "actual_fraud": row[3],
        "anomaly_score": row[4],
        "risk_level": row[5]
    }


# =====================================================
# 4️⃣ ANALYTICS SUMMARY
# =====================================================
@router.get("/analytics/summary")
def analytics_summary():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            SUM(CASE WHEN risk_level='HIGH' AND actual_fraud=true THEN 1 ELSE 0 END),
            SUM(CASE WHEN risk_level='HIGH' AND actual_fraud=false THEN 1 ELSE 0 END),
            SUM(CASE WHEN risk_level!='HIGH' AND actual_fraud=true THEN 1 ELSE 0 END),
            SUM(CASE WHEN risk_level!='HIGH' AND actual_fraud=false THEN 1 ELSE 0 END)
        FROM transactions
        """
    )

    tp, fp, fn, tn = cur.fetchone()
    cur.close()
    conn.close()

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    return {
        "metrics": {
            "precision": round(precision, 3),
            "recall": round(recall, 3)
        }
    }


# =====================================================
# 5️⃣ RISK DISTRIBUTION
# =====================================================
@router.get("/analytics/risk-distribution")
def risk_distribution():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            risk_level,
            COUNT(*),
            SUM(CASE WHEN actual_fraud=true THEN 1 ELSE 0 END)
        FROM transactions
        GROUP BY risk_level
        ORDER BY risk_level
        """
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "risk_level": r[0],
            "total_transactions": r[1],
            "fraud_transactions": r[2]
        }
        for r in rows
    ]


# =====================================================
# 6️⃣ DAY 4C — MOCK GENAI EXPLANATION (POLISHED)
# =====================================================
@router.get("/transactions/{transaction_id}/explain")
def explain_transaction(transaction_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            amount,
            actual_fraud,
            anomaly_score,
            risk_level
        FROM transactions
        WHERE id = %s
        """,
        (transaction_id,)
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {"message": "Transaction not found"}

    amount, actual_fraud, anomaly_score, risk_level = row

    explanation = (
        f"This transaction is classified as {risk_level} risk. "
        f"The transaction amount is {amount}, which deviates from normal behavior. "
    )

    if anomaly_score:
        explanation += (
            f"It has an anomaly score of {round(anomaly_score, 2)}, "
            "indicating unusual activity. "
        )

    if actual_fraud:
        explanation += "Historical data confirms this transaction as fraudulent. "

    explanation += "These factors together contributed to the risk assessment."

    return {
        "transaction_id": transaction_id,
        "risk_level": risk_level,
        "explanation": explanation
    }
