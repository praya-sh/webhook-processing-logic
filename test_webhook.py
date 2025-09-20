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
    headers = {"Content-Type": content_type}
    if sig:
        signature = generate_signature(payload)
        headers["X-signature"] = f"sha256={signature}"
    response = requests.post(WEBHOOK_URL, data=payload, headers=headers)
    print(f"Payload ({content_type}):\n{payload}")
    print(f"Status Code: {response.status_code}\nResponse: {response.text}")
    return response