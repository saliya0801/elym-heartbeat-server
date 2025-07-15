from flask import Flask, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(data)

@app.route("/")
def render():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["timestamp"] = datetime.utcnow().isoformat()
    return render_template("base.html", core_text=data["core"], core_code=data["id"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
