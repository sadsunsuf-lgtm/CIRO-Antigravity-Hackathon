"""
CIRO API — /api/health
Vercel Serverless Function (Python)
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response_body = json.dumps({
            "ok": True,
            "model_ready": False,
            "mode": "lightweight",
            "message": "CIRO backend is online. Running in AI-lite mode (smart keyword matching).",
            "version": "2.0.0-pakistan"
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        pass
