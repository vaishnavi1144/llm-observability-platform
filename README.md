\# 🚀 LLM Observability Platform



A full-stack observability system for tracking, logging, and visualizing LLM (Large Language Model) interactions in real-time.



This project captures prompts, responses, latency, status, and errors from LLM calls and stores them in a structured backend for monitoring and analysis.



\---



\## 📌 Features



\- 🔹 Real-time LLM request logging

\- 🔹 Custom SDK for instrumentation

\- 🔹 FastAPI backend for log ingestion

\- 🔹 SQLite database for storage

\- 🔹 Gradio-based chat frontend

\- 🔹 Streamlit dashboard for visualization

\- 🔹 Latency tracking per request

\- 🔹 Error tracking support



\---



\## 🏗️ Architecture



Frontend (Gradio Chat UI)

↓

SDK Logger (Python Client)

↓

FastAPI Backend (/log endpoint)

↓

SQLite Database (logs.db)

↓

Streamlit Dashboard (Analytics UI)



Frontend (Gradio Chat UI)

↓

SDK Logger (Python Client)

↓

FastAPI Backend (/log endpoint)

↓

SQLite Database (logs.db)

↓

Streamlit Dashboard (Analytics UI)



\---



\## ⚙️ Tech Stack



\- Python

\- FastAPI

\- Gradio

\- Streamlit

\- SQLite

\- Requests

\- Groq API (LLM Provider)



\---



\## 📂 Project Structure



```



llm-observability/

│

├── frontend/        # Gradio chat interface

├── backend/         # FastAPI server

├── sdk/             # Logging SDK

├── dashboard/       # Streamlit analytics UI

├── db/              # Database schema

├── run.py           # One-click runner (optional)

├── requirements.txt

└── README.md



\## 🚀 How to Run



Backend:

uvicorn backend.main:app --reload



Frontend:

python frontend/app.py



Dashboard:

streamlit run dashboard/app.py

