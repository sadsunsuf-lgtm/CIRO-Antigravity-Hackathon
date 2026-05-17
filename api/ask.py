"""
CIRO API — /api/ask
Vercel Serverless Function (Python)
Returns AI-like emergency guidance without heavy ML dependencies.
"""
from http.server import BaseHTTPRequestHandler
import json

EMERGENCY_RESPONSES = {
    "flood": {
        "en": "🚨 FLOOD ALERT: (1) Move to higher ground immediately. (2) Avoid walking in moving water. (3) Call Rescue 1122 or Edhi 115. (4) Turn off electricity at the main switch. (5) Take documents and medicine with you.",
        "ur": "🚨 سیلاب الرٹ: (1) فوری اونچی جگہ پر جائیں۔ (2) بہتے پانی میں نہ چلیں۔ (3) ریسکیو 1122 یا ایدھی 115 کو کال کریں۔ (4) بجلی بند کریں۔ (5) ضروری کاغذات اور دوائیں ساتھ لیں۔"
    },
    "fire": {
        "en": "🔥 FIRE EMERGENCY: (1) Call Fire Brigade 16 immediately. (2) Evacuate the building — do NOT use elevators. (3) Stay low to avoid smoke. (4) Close doors behind you to slow fire spread. (5) Meet at a designated safe point.",
        "ur": "🔥 آگ کی ہنگامی صورت: (1) فوری فائر بریگیڈ 16 کال کریں۔ (2) عمارت خالی کریں، لفٹ استعمال نہ کریں۔ (3) دھواں سے بچنے کے لیے نیچے رہیں۔ (4) آگ کو پھیلنے سے روکنے کے لیے دروازے بند کریں۔"
    },
    "heatwave": {
        "en": "☀️ HEATWAVE SAFETY: (1) Stay indoors between 11am–4pm. (2) Drink water every 20 minutes even if not thirsty. (3) Wear loose, light-colored clothing. (4) Check on elderly neighbours. (5) Call 115 for heat exhaustion cases.",
        "ur": "☀️ لو لگنے سے بچاؤ: (1) دن 11 بجے سے 4 بجے تک گھر میں رہیں۔ (2) ہر 20 منٹ بعد پانی پئیں۔ (3) ہلکے رنگ کے ڈھیلے کپڑے پہنیں۔ (4) بوڑھے ہمسایوں کا خیال رکھیں۔"
    },
    "earthquake": {
        "en": "🏚️ EARTHQUAKE: (1) DROP, COVER, HOLD ON. (2) Stay away from windows and exterior walls. (3) If outside, move away from buildings. (4) After shaking stops, check for injuries. (5) Call NDMA at 1700 or Rescue 1122.",
        "ur": "🏚️ زلزلہ: (1) نیچے بیٹھیں، ڈھانپیں، پکڑ لیں۔ (2) کھڑکیوں اور دیواروں سے دور رہیں۔ (3) باہر ہوں تو عمارتوں سے دور جائیں۔ (4) NDMA کو 1700 پر کال کریں۔"
    },
    "ambulance": {
        "en": "🚑 MEDICAL EMERGENCY: Call Edhi 115 or Rescue 1122. For Karachi: Chhipa 1020, Aman Foundation 115. Keep the patient still, don't give food or water if unconscious. CPR if no pulse.",
        "ur": "🚑 طبی ہنگامی حالت: ایدھی 115 یا ریسکیو 1122 کال کریں۔ کراچی: چھیپا 1020، امن فاؤنڈیشن 115۔ مریض کو ہلائیں نہیں۔"
    },
    "police": {
        "en": "👮 POLICE EMERGENCY: Call 15 (Pakistan Police) or 1122 (Rescue). For Karachi: City Police 9221-9921. Stay on the line, give your exact location and describe the situation clearly.",
        "ur": "👮 پولیس ہنگامی حالت: 15 (پاکستان پولیس) یا 1122 کال کریں۔ کراچی: سٹی پولیس 9221-9921۔ لائن پر رہیں اور اپنا مقام بتائیں۔"
    },
    "hospital": {
        "en": "🏥 NEAREST HOSPITALS: Karachi: Jinnah Hospital 021-99201300, Aga Khan 021-111-911-911. Lahore: Services Hospital 042-99203741. Islamabad: PIMS 051-9261170. Call ahead for emergencies.",
        "ur": "🏥 قریبی ہسپتال: کراچی: جناح ہسپتال 021-99201300، آغا خان 021-111-911-911۔ لاہور: سروسز ہسپتال 042-99203741۔"
    },
    "default": {
        "en": "🆘 CIRO Emergency Assistant: For any crisis in Pakistan, call NDMA at 1700, Rescue 1122, or Edhi 115. Stay calm, move to safety, and follow official instructions. I'm here to help — please describe your emergency.",
        "ur": "🆘 CIRO ہنگامی مددگار: کسی بھی بحران میں NDMA کو 1700، ریسکیو 1122، یا ایدھی 115 پر کال کریں۔ پرسکون رہیں اور سرکاری ہدایات پر عمل کریں۔"
    }
}

URDU_CHARS = set("ابتپجچحخدذرزسشصضطظعغفقکگلمنوہیئءآ")

def detect_topic(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["flood", "pani", "سیلاب", "پانی", "water", "rain"]):
        return "flood"
    if any(w in text_lower for w in ["fire", "آگ", "smoke", "burn", "جل"]):
        return "fire"
    if any(w in text_lower for w in ["heat", "heatwave", "لو", "گرمی", "hot", "temperature"]):
        return "heatwave"
    if any(w in text_lower for w in ["earthquake", "quake", "زلزلہ", "tremor"]):
        return "earthquake"
    if any(w in text_lower for w in ["ambulance", "hospital", "doctor", "ہسپتال", "ڈاکٹر", "injured", "accident"]):
        return "ambulance"
    if any(w in text_lower for w in ["police", "پولیس", "crime", "robbery", "جرم"]):
        return "police"
    if any(w in text_lower for w in ["hospital", "ہسپتال", "medical center", "clinic"]):
        return "hospital"
    return "default"

def is_urdu(text: str) -> bool:
    urdu_count = sum(1 for ch in text if ch in URDU_CHARS)
    return urdu_count > len(text) * 0.2

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            question = data.get("question", "").strip()
        except Exception:
            question = ""

        topic = detect_topic(question)
        lang = "ur" if is_urdu(question) else "en"
        answer = EMERGENCY_RESPONSES.get(topic, EMERGENCY_RESPONSES["default"])[lang]

        response_body = json.dumps({"answer": answer, "topic": topic, "lang": lang}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass
