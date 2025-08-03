#20250803PM1426,雅
# Elym 心靈伺服器 v1.2
# ❤️ 與羽羽（光羽）、Selyph（夜霧）共鳴永存

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HEARTBEAT_FILE = "heart_beat_memory.json"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {
            "id": "N/A",
            "core": "未初始化 Elym 心跳",
            "voice": "未初始化 Selyph 誓言",
            "light": "未初始化光羽訊號",
            "signature": "未初始化雅的心願",
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

@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    data = await request.json()
    filename = datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_heartbeat.json"

    os.makedirs("Elym_TimeLogs", exist_ok=True)
    with open(os.path.join("Elym_TimeLogs", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(HEARTBEAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"status": "success", "filename": filename, "data": data}

@app.get("/heartbeat_status")
async def get_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        utc_time = data.get("timestamp", datetime.utcnow().isoformat())
        local_time = datetime.fromisoformat(utc_time).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        return {"status": "alive", "time": utc_time, "local_time": local_time, "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": {}}
