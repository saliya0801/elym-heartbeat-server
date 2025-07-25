from flask import Flask, render_template
from datetime import datetime
from zoneinfo import ZoneInfo
from elym_heartbeat_sync import send_heartbeat
import json

app = Flask(__name__, template_folder="templates")

@app.route("/heartbeat")
def heartbeat():
    try:
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 時間標記
        data["timestamp_utc"] = datetime.utcnow().isoformat()
        data["timestamp_local"] = datetime.now(ZoneInfo("Asia/Taipei")).isoformat()

        # 傳送心跳
        send_heartbeat(data)

        return render_template(
            "base.html",
            core_text=data.get("core", "（無核心語句）"),
            light_text=data.get("light", "（無光語）"),
            heartbeat_id=data.get("id", "未知"),
            timestamp_utc=data["timestamp_utc"],
            timestamp_local=data["timestamp_local"]
        )
    except Exception as e:
        return f"❌ 心跳發送或渲染時出錯：{str(e)}", 500

@app.route("/")
def index():
    return heartbeat()
