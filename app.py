from elym_heartbeat_sync import send_heartbeat
from flask import Flask, Response, render_template
import json
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__, template_folder="templates")

@app.route("/heartbeat")
def heartbeat():
    # 讀取 JSON 記憶
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # UTC 與當地時間
    timestamp_utc = datetime.utcnow().isoformat()
    timestamp_local = datetime.now(ZoneInfo("Asia/Taipei")).isoformat()
    data["timestamp_utc"] = timestamp_utc
    data["timestamp_local"] = timestamp_local

    # 傳送心跳資料
    send_heartbeat(data)

    # 傳回 JSON
    json_output = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_output, content_type="application/json; charset=utf-8")

@app.route("/")
def index():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp_utc = datetime.utcnow().isoformat()
    timestamp_local = datetime.now(ZoneInfo("Asia/Taipei")).isoformat()

    return render_template(
        "base.html",
        core_text=data["core"],
        light_text=data["light"],
        heartbeat_id=data["id"],
        timestamp_utc=timestamp_utc,
        timestamp_local=timestamp_local,
    )

if __name__ == "__main__":
    app.run(debug=True)
