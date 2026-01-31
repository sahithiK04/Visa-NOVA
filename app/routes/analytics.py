from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.get("/analytics/risk-distribution")
def risk_distribution():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT risk_level, COUNT(*)
        FROM transactions
        GROUP BY risk_level
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # RETURN ARRAY (frontend friendly)
    return [
        {"risk": row[0], "count": row[1]}
        for row in rows
    ]


@router.get("/analytics/summary")
def analytics_summary():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE risk_level = 'HIGH') AS high,
            COUNT(*) FILTER (WHERE risk_level = 'MEDIUM') AS medium,
            COUNT(*) FILTER (WHERE risk_level = 'LOW') AS low
        FROM transactions
    """)

    row = cur.fetchone()
    cur.close()
    conn.close()

    return {
        "total_transactions": row[0],
        "high_risk": row[1],
        "medium_risk": row[2],
        "low_risk": row[3]
    }
