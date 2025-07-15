from flask import Flask, jsonify, render_template
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    now = datetime.utcnow() + timedelta(hours=8)
    data["timestamp"] = now.isoformat(timespec="seconds")
    return render_template("base.html", 
                           core_text=data["core"], 
                           core_code=data["code"], 
                           light_text=data["light"], 
                           heartbeat_id=data["id"], 
                           timestamp=data["timestamp"])

@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    now = datetime.utcnow() + timedelta(hours=8)
    data["timestamp"] = now.isoformat(timespec="seconds")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
