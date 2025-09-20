import requests
import json
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:5000/webhook/camera")
SECRET = os.getenv("WEBHOOK_SECRET", "default_secret")

def generate_signature(payload: str) -> str:
    return hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

def send_webhook(payload: str, content_type="application/json", sig= True):
    