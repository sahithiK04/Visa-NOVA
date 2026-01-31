from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from app.db import get_db
import traceback

router = APIRouter()

@router.post("/transactions/upload")
def upload_transactions(file: UploadFile = File(...)):
    try:
        # Log file received
        print("📥 File received:", file.filename)

        # Read CSV
        df = pd.read_csv(file.file)
        print("✅ CSV loaded. Rows:", len(df))
        print("📊 Columns:", df.columns.tolist())

        # DB connection
        conn = get_db()
        cur = conn.cursor()

        # Insert rows
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO transactions (
                    time_seconds, amount,
                    v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,
                    v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,
                    v21,v22,v23,v24,v25,v26,v27,v28,
                    actual_fraud
                ) VALUES (
                    %s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,
                    %s
                )
                """,
                (
                    int(row["Time"]),
                    float(row["Amount"]),
                    float(row["V1"]), float(row["V2"]), float(row["V3"]), float(row["V4"]), float(row["V5"]),
                    float(row["V6"]), float(row["V7"]), float(row["V8"]), float(row["V9"]), float(row["V10"]),
                    float(row["V11"]), float(row["V12"]), float(row["V13"]), float(row["V14"]), float(row["V15"]),
                    float(row["V16"]), float(row["V17"]), float(row["V18"]), float(row["V19"]), float(row["V20"]),
                    float(row["V21"]), float(row["V22"]), float(row["V23"]), float(row["V24"]), float(row["V25"]),
                    float(row["V26"]), float(row["V27"]), float(row["V28"]),
                    True if int(row["Class"]) == 1 else False
                )
            )

        # Commit and close
        conn.commit()
        cur.close()
        conn.close()

        return {"message": f"{len(df)} transactions uploaded successfully"}

    except Exception as e:
        print("❌ ERROR OCCURRED DURING UPLOAD")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
