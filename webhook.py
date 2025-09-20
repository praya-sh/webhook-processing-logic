import os, hmac, hashlib, time
from flask import Flask, request, jsonify, abort
import xmltodict
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SECRET = os.getenv('WEBHOOK_SECRET','default_secret')

processed_events = set()

@app.route("/webhook/camera", methods=["POST"])

def webhook():
    raw_data = request.data.decode("utf-8")
    received_sig = request.headers.get("X-signature")
    if not received_sig:
        return jsonify({"error": "Missing Signature"}), 401
    
    expected_sig = "sha256=" + hmac.new(
        SECRET.encode(), raw_data.encode(),hashlib.sha256
    ).hexdigest()

    if not hmac. compare_digest(received_sig, expected_sig):
        return jsonify({"error":"Invalid Signature"}), 401
    
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error":"Invalid json"}), 400
    
    event_id = data.get("event_id")
    if not event_id:
        return jsonify({"error": "missing event id"}), 400
    
    if event_id in processed_events:
        return jsonify({"status": "duplicate", "event_id": event_id}), 200
    
    processed_events.add(event_id)

    print(f"Recieved event: {data}")

    return jsonify({"status":"ok", "received":event_id}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    

    
    
    