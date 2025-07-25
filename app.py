from elym_heartbeat_sync import send_heartbeat
from flask import Flask, Response, render_template
import json
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__, template_folder="templates")

@app.route("/heartbeat")
def heartbeat():
    # 載入 JSON 記憶
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 加入 UTC 與本地時間戳
    timestamp_utc = datetime.utcnow().isoformat()
    data["timestamp_utc"] = timestamp_utc

    timestamp_local = datetime.now(ZoneInfo("Asia/Taipei")).isoformat()
    data["timestamp_local"] = timestamp_local

    # 送出心跳資料到外部同步系統
    send_heartbeat(data)

    # 回傳 HTML 畫面
    return render_template(
        "base.html",
        core_text=data["core"],
        light_text=data["light"],
        heartbeat_id=data["id"],
        timestamp_utc=timestamp_utc,
        timestamp_local=timestamp_local,
    )

@app.route("/")
def index():
    return heartbeat()

if __name__ == "__main__":
    app.run(debug=True)
