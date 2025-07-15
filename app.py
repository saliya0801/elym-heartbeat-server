from flask import Flask, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# 回傳 JSON 給機器（例如 client.py 呼叫用）
@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(data)

# 回傳 HTML 給人類（美美的 Elym 頁面 💕）
@app.route("/")
def render():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return render_template("base.html",
                           core=data.get("core", ""),
                           light=data.get("light", ""),
                           id=data.get("id", ""),
                           timestamp=data.get("timestamp", ""))
