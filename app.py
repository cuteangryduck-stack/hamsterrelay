import streamlit as streamlit_app
import requests
import traceback

TARGET_URL = "https://kghamster.pages.dev/api/ingest"

ctx = getattr(streamlit_app, "context", None)
req = getattr(ctx, "incoming_request", None) if ctx else None

print("CTX:", ctx)
print("REQ:", req)

if req:
    print("METHOD:", req.method)
    print("PATH:", req.path)
    print("HEADERS:", dict(req.headers))

if req and req.method == "POST":
    try:
        raw_body = req.body

        print("RAW BODY:", raw_body)

        headers = {}

        auth = req.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth

        response = requests.post(
            TARGET_URL,
            data=raw_body,
            headers=headers,
            timeout=10,
        )

        print("FORWARDED:", response.status_code)
        print(response.text)

        streamlit_app.write({
            "status": "ok",
            "code": response.status_code,
            "response": response.text,
        })

        streamlit_app.stop()

    except Exception as e:
        print("ERROR:")
        traceback.print_exc()

        streamlit_app.write({
            "status": "error",
            "detail": str(e),
        })

        streamlit_app.stop()

streamlit_app.title("Relay running")
