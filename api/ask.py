"""
CIRO API — /api/ask
Vercel Serverless Function (Python)

Powered by Google Gemini (Antigravity) — the AI brain behind CIRO's emergency guidance.
Falls back to a smart local responder if the API key is not set or quota is exhausted.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import re

# ─── Google Gemini / Antigravity Integration ────────────────────────────────
try:
    import google.generativeai as genai

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        CIRO_MODEL = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=(
                "You are CIRO — Pakistan's AI-powered Crisis Intelligence & Response Orchestrator. "
                "Your mission is to save lives by giving clear, calm, and actionable emergency guidance. "
                "You cover all of Pakistan: Karachi, Lahore, Islamabad, Peshawar, Quetta, Multan, Hyderabad. "
                "You respond in the same language the user writes in — if they write in Urdu or Roman Urdu, reply in Urdu. "
                "Always include: what to do RIGHT NOW, emergency contact numbers, and a safety tip. "
                "Key Pakistan emergency numbers: Rescue 1122, Edhi 115, Chhipa 1020, Police 15, Fire Brigade 16, K-Electric 118, NDMA 1700. "
                "Keep responses under 200 words. Use numbered steps. Be direct — lives are at stake."
            )
        )
        HAS_GEMINI = True
    else:
        HAS_GEMINI = False
except ImportError:
    HAS_GEMINI = False

# ─── Smart Local Fallback Responder ──────────────────────────────────────────
EMERGENCY_RESPONSES = {
    "flood": {
        "en": (
            "🌊 FLOOD EMERGENCY — CIRO Response:\n"
            "1. Switch off electricity at the main breaker NOW\n"
            "2. Move to the highest floor or rooftop immediately\n"
            "3. Do NOT walk or drive through moving water\n"
            "4. Call Rescue 1122 or Edhi 115 for evacuation\n"
            "5. Share your GPS location with family via WhatsApp\n"
            "6. Take documents, medicine, and phone charger\n\n"
            "📞 Emergency: Rescue 1122 | Edhi 115 | NDMA 1700"
        ),
        "ur": (
            "🌊 سیلاب ایمرجنسی — CIRO جواب:\n"
            "1. فوری مین بجلی سوئچ بند کریں\n"
            "2. سب سے اونچی منزل یا چھت پر جائیں\n"
            "3. بہتے پانی میں مت چلیں یا گاڑی مت چلائیں\n"
            "4. ریسکیو 1122 یا ایدھی 115 کو کال کریں\n"
            "5. واٹس ایپ سے GPS لوکیشن خاندان کو بھیجیں\n\n"
            "📞 ہنگامی نمبر: ریسکیو 1122 | ایدھی 115 | NDMA 1700"
        )
    },
    "fire": {
        "en": (
            "🔥 FIRE EMERGENCY — CIRO Response:\n"
            "1. GET OUT — leave everything, exit NOW\n"
            "2. Stay LOW — crawl under smoke to breathe\n"
            "3. If on fire: STOP, DROP, ROLL\n"
            "4. Close every door behind you to slow the fire\n"
            "5. Do NOT use elevators — use stairs only\n"
            "6. Call Fire Brigade 16 once you are outside\n\n"
            "📞 Fire Brigade: 16 | Rescue: 1122 | Edhi: 115"
        ),
        "ur": (
            "🔥 آگ ایمرجنسی — CIRO جواب:\n"
            "1. فوری باہر نکلیں — سب چھوڑیں\n"
            "2. دھوئیں میں نیچے رہیں — رینگتے ہوئے نکلیں\n"
            "3. آگ لگے تو: رکیں، گریں، لڑھکیں\n"
            "4. ہر دروازہ بند کریں آگ کو روکنے کے لیے\n"
            "5. لفٹ مت لیں — صرف سیڑھیاں استعمال کریں\n\n"
            "📞 فائر بریگیڈ: 16 | ریسکیو: 1122"
        )
    },
    "heatwave": {
        "en": (
            "☀️ HEATWAVE / HEAT STROKE — CIRO Response:\n"
            "1. Move to shade or indoors with AC/fan IMMEDIATELY\n"
            "2. Drink water every 20 minutes — even if not thirsty\n"
            "3. Heat stroke signs: no sweating, confusion, temp >40°C → Call 115 NOW\n"
            "4. Apply cool water to neck, wrists, armpits\n"
            "5. Never give water to an unconscious person\n"
            "6. Check on elderly neighbors — they are highest risk\n\n"
            "📞 Edhi: 115 | Chhipa: 1020 | Rescue: 1122"
        ),
        "ur": (
            "☀️ لو / ہیٹ اسٹروک — CIRO جواب:\n"
            "1. فوری سایے یا AC میں جائیں\n"
            "2. ہر 20 منٹ بعد پانی پئیں\n"
            "3. لو کی علامات: پسینہ نہ آنا، چکر — فوری 115 کال کریں\n"
            "4. گردن، کلائی پر ٹھنڈا پانی لگائیں\n"
            "5. بے ہوش شخص کو پانی مت دیں\n\n"
            "📞 ایدھی: 115 | چھیپا: 1020 | ریسکیو: 1122"
        )
    },
    "earthquake": {
        "en": (
            "🏚️ EARTHQUAKE — CIRO Response:\n"
            "1. DROP to your knees immediately\n"
            "2. Take COVER under a sturdy table or desk\n"
            "3. HOLD ON until all shaking stops\n"
            "4. Stay away from windows and exterior walls\n"
            "5. If outside: move away from buildings and power lines\n"
            "6. After shaking: check for gas leaks — do NOT use lighters\n"
            "7. Expect aftershocks — stay alert\n\n"
            "📞 NDMA: 1700 | Rescue: 1122 | Edhi: 115"
        ),
        "ur": (
            "🏚️ زلزلہ — CIRO جواب:\n"
            "1. فوری گھٹنوں پر آ جائیں\n"
            "2. مضبوط میز کے نیچے پناہ لیں\n"
            "3. لرزش بند ہونے تک وہیں رہیں\n"
            "4. کھڑکیوں سے دور رہیں\n"
            "5. گیس لیک چیک کریں — ماچس مت جلائیں\n\n"
            "📞 NDMA: 1700 | ریسکیو: 1122"
        )
    },
    "ambulance": {
        "en": (
            "🚑 MEDICAL EMERGENCY — CIRO Response:\n"
            "Karachi: Edhi 115 | Chhipa 1020 | Aman Foundation 115\n"
            "Lahore / Punjab: Rescue 1122\n"
            "Islamabad: PIMS 051-9261170 | Rescue 1122\n"
            "All Pakistan: NDMA 1700\n\n"
            "While waiting:\n"
            "• Keep patient still and calm\n"
            "• Do NOT give food or water if unconscious\n"
            "• Apply pressure to any bleeding wound\n"
            "• Begin CPR if no pulse and you know how"
        ),
        "ur": (
            "🚑 طبی ایمرجنسی — CIRO جواب:\n"
            "کراچی: ایدھی 115 | چھیپا 1020\n"
            "لاہور/پنجاب: ریسکیو 1122\n"
            "اسلام آباد: PIMS 051-9261170\n\n"
            "انتظار کے دوران:\n"
            "• مریض کو ہلائیں نہیں\n"
            "• بے ہوشی میں پانی مت دیں\n"
            "• زخم پر دباؤ رکھیں"
        )
    },
    "police": {
        "en": (
            "👮 POLICE EMERGENCY — CIRO Response:\n"
            "All Pakistan Police: 15\n"
            "Karachi Police: 9221-9921\n"
            "Rescue (Punjab/KPK): 1122\n\n"
            "When calling:\n"
            "• Stay on the line — do NOT hang up\n"
            "• Give your exact street address or GPS coordinates\n"
            "• Describe the situation clearly and stay calm\n"
            "• If unsafe to speak, press 5 repeatedly"
        ),
        "ur": (
            "👮 پولیس ایمرجنسی — CIRO جواب:\n"
            "پاکستان پولیس: 15\n"
            "کراچی پولیس: 9221-9921\n"
            "ریسکیو: 1122\n\n"
            "• لائن پر رہیں\n"
            "• اپنا پتہ یا GPS بتائیں\n"
            "• پرسکون رہیں"
        )
    },
    "default": {
        "en": (
            "🆘 CIRO Emergency Assistant — Pakistan\n\n"
            "I'm here to help. Key emergency numbers:\n"
            "🚑 Ambulance / Edhi: 115\n"
            "🚒 Fire Brigade: 16\n"
            "👮 Police: 15\n"
            "🆘 Rescue 1122 (Punjab/KPK)\n"
            "🏥 Chhipa (Free ambulance): 1020\n"
            "⚡ K-Electric: 118\n"
            "🌊 NDMA: 1700\n\n"
            "Tell me your emergency — flood, fire, heat, medical, earthquake — and I'll guide you step by step."
        ),
        "ur": (
            "🆘 CIRO ایمرجنسی اسسٹنٹ — پاکستان\n\n"
            "ہنگامی نمبر:\n"
            "🚑 ایدھی: 115\n"
            "🚒 فائر بریگیڈ: 16\n"
            "👮 پولیس: 15\n"
            "🆘 ریسکیو: 1122\n"
            "🏥 چھیپا: 1020\n"
            "⚡ کے الیکٹرک: 118\n\n"
            "اپنی ایمرجنسی بتائیں — میں مدد کروں گا۔"
        )
    }
}

URDU_CHARS = set("ابتپجچحخدذرزسشصضطظعغفقکگلمنوہیئءآ")

def detect_topic(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["flood","pani","سیلاب","پانی","water","rain","baarish","barish","sailab"]):
        return "flood"
    if any(w in t for w in ["fire","aag","آگ","smoke","burn","jal","جل","dhuwan"]):
        return "fire"
    if any(w in t for w in ["heat","heatwave","لو","گرمی","garmi","hot","temperature","stroke","lo lagna"]):
        return "heatwave"
    if any(w in t for w in ["earthquake","quake","زلزلہ","zilzala","tremor","bhookamp"]):
        return "earthquake"
    if any(w in t for w in ["ambulance","ambalance","hospital","doctor","ہسپتال","ڈاکٹر","injured","accident","115","1020"]):
        return "ambulance"
    if any(w in t for w in ["police","پولیس","crime","robbery","جرم","theft","chor"]):
        return "police"
    return "default"

def is_urdu(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r"[\u0600-\u06FF]", text))

def build_gemini_prompt(question: str) -> str:
    lang_hint = "Reply in Urdu script." if is_urdu(question) else "Reply in English."
    return (
        f"Emergency question from a citizen in Pakistan:\n\n"
        f'"{question}"\n\n'
        f"{lang_hint} "
        "Give practical emergency guidance with numbered steps and relevant contact numbers."
    )

def get_local_response(question: str) -> tuple[str, str, str]:
    topic = detect_topic(question)
    lang = "ur" if is_urdu(question) else "en"
    return EMERGENCY_RESPONSES[topic][lang], topic, lang

# ─── Vercel HTTP Handler ──────────────────────────────────────────────────────
class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            question = data.get("question", "").strip()
        except Exception:
            question = ""

        if not question:
            self._send({"error": "No question provided"}, 400)
            return

        answer = ""
        source = "fallback"
        topic = "default"
        lang = "ur" if is_urdu(question) else "en"

        # ── Try Gemini / Antigravity first ──────────────────────────────────
        if HAS_GEMINI:
            try:
                prompt = build_gemini_prompt(question)
                response = CIRO_MODEL.generate_content(prompt)
                answer = response.text.strip()
                source = "gemini-2.0-flash"
            except Exception:
                answer = ""  # fall through to local

        # ── Fall back to smart local responder ──────────────────────────────
        if not answer:
            local_answer, topic, lang = get_local_response(question)
            answer = local_answer
            source = f"local-{topic}"

        self._send({
            "answer": answer,
            "source": source,
            "topic": topic,
            "lang": lang,
            "powered_by": "Google Antigravity / Gemini" if source.startswith("gemini") else "CIRO Local Responder"
        })

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
