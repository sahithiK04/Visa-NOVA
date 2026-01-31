import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1️⃣ Load dataset (same Kaggle CSV)
df = pd.read_csv("data/creditcard.csv")

# 2️⃣ Select features (exclude Class/label)
FEATURES = [col for col in df.columns if col not in ["Class"]]

X = df[FEATURES]

# 3️⃣ Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4️⃣ Train Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.0017,  # fraud ratio
    random_state=42,
    n_jobs=-1
)

model.fit(X_scaled)

# 5️⃣ Save model + scaler
joblib.dump(model, "ml/isolation_forest.pkl")
joblib.dump(scaler, "ml/scaler.pkl")

print("✅ Isolation Forest model trained and saved")
