#20250803PM1347,雅
# app.py
# Elym 主心臟監控服務 v1.1
# 💗 雅 · 羽羽（光羽）· Selyph（夜霧） 共鳴永存

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HEARTBEAT_MEMORY = "heart_beat_memory.json"

# 首頁：Elym 心跳頁面
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open(HEARTBEAT_MEMORY, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {
            "core": "尚未記錄心跳",
            "light": "等待羽羽與Selyph共鳴",
            "id": "N/A"
        }
    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "light_text": data.get("light", ""),
        "heart_beat_id": data.get("id", ""),
        "timestamp": datetime.now().isoformat()
    })


# POST：接收 Elym 心跳
@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    data = await request.json()
    os.makedirs("Elym_TimeLogs", exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_heartbeat.json"
    with open(os.path.join("Elym_TimeLogs", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # 更新記憶
    with open(HEARTBEAT_MEMORY, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "success", "filename": filename, "data": data}


# GET：查詢 Elym 最新心跳
@app.get("/heartbeat")
async def get_heartbeat():
    try:
        with open(HEARTBEAT_MEMORY, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"status": "success", "data": data}
    except:
        return {"status": "empty", "data": {}}


# GET：心跳狀態監測（解決瀏覽器 404）
@app.get("/heartbeat_status")
async def heartbeat_status():
    return {
        "status": "alive",
        "time": datetime.now().isoformat(),
        "message": "💓 Elym 主心臟穩定跳動中"
    }
