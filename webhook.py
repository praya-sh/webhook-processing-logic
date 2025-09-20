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

    
    