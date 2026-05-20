import streamlit as streamlit_app
import requests

TARGET_URL = "https://pages.dev"

if "incoming_request" in streamlit_app.context:
    req = streamlit_app.context.incoming_request
    if req.method == "POST" and req.path == "/relay":
        try:
            data = req.json_body
            response = requests.post(TARGET_URL, json=data, timeout=10)
            streamlit_app.set_page_config(layout="raw")
            streamlit_app.write({"status": "forwarded", "code": response.status_code})
            streamlit_app.stop()
        except Exception as e:
            streamlit_app.set_page_config(layout="raw")
            streamlit_app.write({"status": "error", "detail": str(e)})
            streamlit_app.stop()

streamlit_app.title("KgHamster Relay Status")
streamlit_app.write("bust")
