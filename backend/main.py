from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

# ----------------------------
# DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id TEXT,
    model TEXT,
    provider TEXT,
    prompt TEXT,
    response TEXT,
    latency REAL,
    status TEXT,
    error TEXT,
    timestamp REAL
)
""")

conn.commit()

# ----------------------------
# DATA SCHEMA
# ----------------------------
class Log(BaseModel):
    id: str
    model: str
    provider: str
    prompt: str
    response: str
    latency: float
    status: str
    error: str = ""
    timestamp: float

# ----------------------------
# HEALTH CHECK (ROOT)
# ----------------------------
@app.get("/")
def home():
    return {
        "status": "backend running",
        "message": "LLM Observability API is active"
    }

# ----------------------------
# INGEST LOGS
# ----------------------------
@app.post("/log")
def ingest(log: Log):

    # 🔥 DEBUG LOGS (VISIBLE IN TERMINAL)
    print("\n🔥 NEW LOG RECEIVED 🔥")
    print("ID:", log.id)
    print("MODEL:", log.model)
    print("PROMPT:", log.prompt[:200])
    print("RESPONSE:", log.response[:200])
    print("LATENCY:", log.latency)
    print("STATUS:", log.status)
    print("TIME:", log.timestamp)

    # STORE IN DATABASE
    cursor.execute("""
        INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log.id,
        log.model,
        log.provider,
        log.prompt,
        log.response,
        log.latency,
        log.status,
        log.error,
        log.timestamp
    ))

    conn.commit()

    return {
        "status": "stored successfully",
        "id": log.id
    }

# ----------------------------
# GET ALL LOGS (DASHBOARD SUPPORT)
# ----------------------------
@app.get("/logs")
def get_logs():
    rows = cursor.execute(
        "SELECT * FROM logs ORDER BY timestamp DESC"
    ).fetchall()

    return [
        {
            "id": r[0],
            "model": r[1],
            "provider": r[2],
            "prompt": r[3],
            "response": r[4],
            "latency": r[5],
            "status": r[6],
            "error": r[7],
            "timestamp": r[8]
        }
        for r in rows
    ]

# ----------------------------
# BASIC STATS (FOR DASHBOARD)
# ----------------------------
@app.get("/stats")
def stats():
    rows = cursor.execute("SELECT latency, status FROM logs").fetchall()

    if not rows:
        return {
            "total_requests": 0,
            "avg_latency": 0,
            "max_latency": 0,
            "min_latency": 0,
            "error_count": 0
        }

    latencies = [r[0] for r in rows]
    errors = [r for r in rows if r[1] != "success"]

    return {
        "total_requests": len(rows),
        "avg_latency": sum(latencies) / len(latencies),
        "max_latency": max(latencies),
        "min_latency": min(latencies),
        "error_count": len(errors)
    }