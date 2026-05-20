import threading
from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import streamlit as streamlit_app

app = FastAPI()

TARGET_URL = "https://pages.dev"

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.post("/relay")
async def relay_log(data: dict):
    try:
        response = requests.post(TARGET_URL, json=data, timeout=10)
        return {"status": "forwarded", "code": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if "server_started" not in streamlit_app.session_state:
    streamlit_app.session_state.server_started = True
    threading.Thread(target=run_server, daemon=True).start()

streamlit_app.title("KgHamster Relay Status")
streamlit_app.write("The backend is active")
