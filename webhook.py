import os, hmac, hashlib, time
from flask import Flask, request, jsonify, abort
import xmltodict
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SECRET = os.getenv('WEBHOOK_SECRET','default_secret')

processed_events = set()

@app.route("/webhook/camera", methods=["POST"])


    