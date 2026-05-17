import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

MODEL_ID = "google/flan-t5-small"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "mobile_app")

class AskRequest(BaseModel):
    question: str

app = FastAPI(title="CIRO AI Backend", docs_url="/api/docs")

model_ready = False
model = None
tokenizer = None

@app.on_event("startup")
async def load_model():
    global tokenizer, model, model_ready
    if HAS_TRANSFORMERS:
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
            model_ready = True
        except Exception as e:
            print("Failed to load model:", e)
            model_ready = False
    else:
        print("Transformers not installed. Running in lightweight mode.")
        model_ready = False


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
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_new_tokens=256, do_sample=False, num_beams=4)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
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

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
