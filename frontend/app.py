import os
import time
import uuid
import requests
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("GROQ KEY LOADED:", bool(GROQ_API_KEY))

client = Groq(api_key=GROQ_API_KEY)

BACKEND_URL = "http://127.0.0.1:8000/log"

# -----------------------------
# SAFE LOGGING FUNCTION
# -----------------------------
def log_to_backend(question, answer, start, end):
    try:
        data = {
            "id": str(uuid.uuid4()),
            "model": "llama-3.3-70b-versatile",
            "provider": "groq",
            "prompt": str(question),
            "response": str(answer),
            "latency": float(end - start),
            "status": "success",
            "error": "",  # IMPORTANT: must NOT be None
            "timestamp": float(time.time())
        }

        print("📤 SENDING LOG:", data)

        res = requests.post(
            BACKEND_URL,
            json=data,
            timeout=2
        )

        print("📥 BACKEND RESPONSE:", res.status_code)

    except Exception as e:
        print("❌ LOG FAILED:", str(e))


# -----------------------------
# CHAT FUNCTION
# -----------------------------
def chat(message, history):
    start = time.time()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Model Error: {str(e)}"

    end = time.time()

    log_to_backend(message, answer, start, end)

    return answer


# -----------------------------
# UI
# -----------------------------
gr.ChatInterface(
    fn=chat,
    title="LLM Observability System 🚀"
).launch()