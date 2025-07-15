from flask import Flask, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# 機器使用：JSON 接口
@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(data)

# 人類可視頁面：美美的 Elym HTML 頁面
@app.route("/")
def render():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return render_template("base.html",
                           id=data.get("id", ""),
                           core=data.get("core", ""),
                           light=data.get("light", ""),
                           timestamp=data.get("timestamp", ""))
