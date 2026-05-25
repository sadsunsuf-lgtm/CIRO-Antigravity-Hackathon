import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
    from google.genai import types
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
        HAS_GEMINI = True
    else:
        HAS_GEMINI = False
except ImportError:
    HAS_GEMINI = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "mobile_app")

class AskRequest(BaseModel):
    question: str

app = FastAPI(title="CIRO AI Backend", docs_url="/api/docs")

model_ready = HAS_GEMINI

@app.on_event("startup")
async def load_model():
    if not HAS_GEMINI:
        print("Gemini API not available. Running in lightweight fallback mode.")
    else:
        print("Gemini API connected successfully.")


def build_prompt(question: str) -> str:
    language_hint = (
        "Answer in Urdu if the user asks in Urdu, otherwise answer in English."
        if any(ch in question for ch in "ابتپکڈی")
        else "Answer in the language the user asks in."
    )

    return (
        "You are CIRO, an emergency assistant for Pakistan. "
        "Provide short, actionable guidance and safety instructions for crises. "
        "Stay calm and practical. "
        f"{language_hint} "
        "If the question is about flood, fire, heat, hospital, ambulance, police, rescue, earthquake, "
        "or safety, give emergency steps, contact numbers, and what to do next. "
        "If the question is not related to immediate emergency response, still provide a safe recommendation.\n\n"
        f"Question: {question}\nAnswer:"
    )

@app.post("/api/ask")
async def ask_ciro(request: AskRequest):
    if not model_ready:
        raise HTTPException(status_code=503, detail="Model is still loading")

    prompt = build_prompt(request.question.strip())
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        answer = response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        answer = ""

    return {"answer": answer}

@app.get("/api/trace")
async def get_trace():
    payload = {}
    for filename in ("agent_trace.json", "live_stream.json"):
        path = os.path.join(ROOT_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                payload[filename.replace(".json", "")] = json.load(fh)
    return payload or {"status": "no-trace", "message": "No trace files found."}

@app.get("/api/health")
async def health():
    return {"ok": True, "model_ready": model_ready}

# Mount the mobile_app directory at root to serve all static files (css, js, images) seamlessly
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
