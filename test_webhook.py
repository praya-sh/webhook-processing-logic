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

def test_valid_json():
    payload = json.dumps({
        "event_id": "evt_001",
        "source_id": "camera-42",
        "type": "motion_detected",
        "ts": "2025-09-19T21:32:10Z"
    })
    send_webhook(payload, "application/json")

def test_missing_fields():
    payload = json.dumps({
        "source_id": "camera-42",
        "type": "motion_detected"
    })  # missing event_id
    send_webhook(payload, "application/json")

def test_invalid_signature():
    payload = json.dumps({
        "event_id": "evt_002",
        "source_id": "camera-42",
        "type": "keepalive",
        "ts": "2025-09-19T21:35:00Z"
    })
    send_webhook(payload, "application/json", sig=False)  # no signature

def test_duplicate_event():
    payload = json.dumps({
        "event_id": "evt_001",  # same as first test
        "source_id": "camera-42",
        "type": "motion_detected",
        "ts": "2025-09-19T21:32:10Z"
    })
    send_webhook(payload, "application/json")

def test_malformed_json():
    payload = '{"event_id": "evt_003", "source_id": "camera-42", "type": "motion_detected", "ts": "2025-09-19T21:36:00Z"'  # missing closing }
    send_webhook(payload, "application/json")

def test_unsupported_content_type():
    payload = "Just some plain text"
    send_webhook(payload, "text/plain")


if __name__ == "__main__":
    print("Starting webhook tests...")
    test_valid_json()
    test_missing_fields()
    test_invalid_signature()
    test_duplicate_event()
    test_malformed_json()
    test_unsupported_content_type()
    print("\nAll tests finished.")