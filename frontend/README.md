# VISA-NOVA – AI-Powered Transaction Intelligence Platform

VISA-NOVA is a full-stack AI-powered transaction intelligence system designed to analyze financial transaction data, detect anomalous behavior, and provide explainable AI insights through an interactive dashboard.

This project uses a real-world fraud dataset and demonstrates end-to-end system design including data ingestion, anomaly detection, analytics, visualization, and GenAI-style explanations.

---

## 🚀 Features

- Upload and process large transaction datasets
- Anomaly detection with risk classification (LOW / MEDIUM / HIGH)
- Fraud analytics (precision, recall, risk distribution)
- Interactive React dashboard with charts and tables
- Explainable AI (GenAI-style) transaction explanations
- Modular FastAPI backend with PostgreSQL

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- psycopg2
- SQL

### Frontend
- React.js
- Recharts (Charts)
- HTML / CSS

### AI / Analytics
- Anomaly Detection (rule-based + scores)
- Risk classification
- Explainable AI (Mock GenAI logic)

---

## 📊 Dashboard Highlights

- KPI cards for model metrics
- Risk distribution charts (Bar & Pie)
- High-risk anomaly monitoring
- Transaction-level drill-down with AI explanations

---

## 🧠 Explainable AI

Each transaction can be explained using a GenAI-style endpoint that produces human-readable reasoning based on:
- Transaction amount
- Anomaly score
- Risk level
- Historical fraud patterns

This design can be easily extended to real LLMs (OpenAI, etc.).

---

## ▶️ How to Run Locally

### 1️⃣ Backend

```bash
cd visa-nova
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# VISA-NOVA – AI-Powered Transaction Intelligence Platform

VISA-NOVA is a full-stack AI-powered transaction intelligence system designed to analyze financial transaction data, detect anomalous behavior, and provide explainable AI insights through an interactive dashboard.

This project uses a real-world fraud dataset and demonstrates end-to-end system design including data ingestion, anomaly detection, analytics, visualization, and GenAI-style explanations.

---

## 🚀 Features

- Upload and process large transaction datasets
- Anomaly detection with risk classification (LOW / MEDIUM / HIGH)
- Fraud analytics (precision, recall, risk distribution)
- Interactive React dashboard with charts and tables
- Explainable AI (GenAI-style) transaction explanations
- Modular FastAPI backend with PostgreSQL

---

## 🏗️ Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- psycopg2
- SQL

### Frontend
- React.js
- Recharts (Charts)
- HTML / CSS

### AI / Analytics
- Anomaly Detection (rule-based + scores)
- Risk classification
- Explainable AI (Mock GenAI logic)

---

## 📊 Dashboard Highlights

- KPI cards for model metrics
- Risk distribution charts (Bar & Pie)
- High-risk anomaly monitoring
- Transaction-level drill-down with AI explanations

---

## 🧠 Explainable AI

Each transaction can be explained using a GenAI-style endpoint that produces human-readable reasoning based on:
- Transaction amount
- Anomaly score
- Risk level
- Historical fraud patterns

This design can be easily extended to real LLMs (OpenAI, etc.).

---

## ▶️ How to Run Locally

### 1️⃣ Backend

```bash
cd visa-nova
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

###Dataset

Credit Card Fraud Detection dataset (Kaggle)

Transactions > 17,000 rows

Real-world imbalanced fraud data

