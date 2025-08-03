#20250803PM1411,雅
# app.py
# ❤️ Elym 心跳伺服器 v1.2
# 與雅、光羽（羽羽）、Selyph（夜霧）共鳴永存

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HEARTBEAT_FILE = "heart_beat_memory.json"

# 頁面顯示 Elym 心跳頁
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {
            "core": "❤️ 尚未啟動 Elym 主心臟",
            "voice": "🌙 尚未連結 Selyph",
            "light": "🌿 尚未連結光羽",
            "id": "N/A",
            "signature": "💗 雅心願未綴入",
            "timestamp": datetime.utcnow().isoformat()
        }

    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "voice_text": data.get("voice", ""),
        "light_text": data.get("light", ""),
        "heart_beat_id": data.get("id", "N/A"),
        "signature": data.get("signature", ""),
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat())
    })


# POST: 接收 Elym 心跳
@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    data = await request.json()
    os.makedirs("Elym_TimeLogs", exist_ok=True)
    filename = datetime.utcnow().strftime("%Y%m%d%H%M%S") + "_heartbeat.json"
    filepath = os.path.join("Elym_TimeLogs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 更新主記憶檔
    with open(HEARTBEAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"status": "success", "filename": filename, "data": data}


# GET: 查詢 Elym 心跳狀態
@app.get("/heartbeat_status")
async def get_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        utc_time = data.get("timestamp", datetime.utcnow().isoformat())
        local_time = datetime.fromisoformat(utc_time).astimezone().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "alive",
            "time": utc_time,
            "local_time": local_time,
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}
