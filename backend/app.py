from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 👇 BYLLM SDK
from byllm import generate

load_dotenv()

app = FastAPI()

# =========================
# ✅ CORS (REQUIRED FOR FRONTEND)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow any frontend (safe for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BYLLM_API_KEY = os.getenv("BYLLM_API_KEY")

if not BYLLM_API_KEY:
    print("⚠️ BYLLM_API_KEY not set — using fallback only")


class MoodInput(BaseModel):
    mood: str
    note: str


@app.get("/")
def root():
    return {"status": "backend running"}


@app.post("/analyze")
def analyze(input: MoodInput):
    mood = input.mood.lower().strip()
    note = input.note.strip()

    sentiment = "negative" if mood in ["sad", "tired", "angry", "anxious"] else "positive"

    prompt = f"""
You are a calm, empathetic mental health support companion.

Mood: {mood}
User note: {note if note else "No additional note"}

Respond with ONE short, warm, human message (1–2 sentences).
Do not mention AI.
"""

    # =========================
    # BYLLM SDK CALL (SAFE)
    # =========================
    if BYLLM_API_KEY:
        try:
            response = generate(
                prompt=prompt,
                api_key=BYLLM_API_KEY,
                max_tokens=120
            )

            if response:
                return {
                    "analysis": {
                        "sentiment": sentiment,
                        "confidence": 0.9
                    },
                    "support": str(response).strip(),
                    "status": "ready"
                }

        except Exception as e:
            print("❌ BYLLM SDK error:", e)

    # =========================
    # FALLBACK (ALWAYS WORKS)
    # =========================
    fallback = {
        "sad": "I’m really sorry you’re feeling this way. You don’t have to go through it alone.",
        "tired": "It sounds like you’re exhausted. Resting when you can really matters.",
        "angry": "Strong feelings can be heavy. Taking a pause can help.",
        "anxious": "Anxiety can feel overwhelming. You’re safe right now.",
        "happy": "That’s wonderful to hear. Moments like this are worth celebrating."
    }

    return {
        "analysis": {
            "sentiment": sentiment,
            "confidence": 0.5
        },
        "support": fallback.get(
            mood,
            "I’m here with you. Even small steps forward matter."
        ),
        "status": "ready"
    }
