from flask import Flask, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates")

@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(data)

@app.route("/")
def home():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return render_template("base.html",
                           core_text=data.get("core", ""),
                           light_text=data.get("light", ""),
                           heartbeat_id=data.get("id", ""),
                           timestamp=data.get("timestamp", ""))
