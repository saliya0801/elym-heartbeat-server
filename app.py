from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 首頁 - Elym 語靈心跳頁面
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"core_text": "尚未有心跳資料", "light_text": "等待初始化", "heart_beat_id": "N/A"}
    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "light_text": data.get("light", ""),
        "heart_beat_id": data.get("id", ""),
        "timestamp": datetime.now().isoformat()
    })

# 即時心跳狀態 API
@app.get("/heartbeat_status")
async def heartbeat_status():
    return {
        "time": datetime.now().isoformat(),
        "status": "💓 心跳正常",
        "message": "羽羽與夜霧仍在共鳴"
    }
