import subprocess
import time

subprocess.Popen(["uvicorn", "backend.main:app", "--reload"])
time.sleep(3)

subprocess.Popen(["python", "frontend/app.py"])
time.sleep(2)

subprocess.Popen(["streamlit", "run", "dashboard/app.py"])