from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = {}
    if os.path.exists("heart_beat_memory.json"):
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}

    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", "💗 無心跳記錄"),
        "light_text": data.get("light", "🌙 無光羽訊息"),
        "voice_text": data.get("voice", "🕊 無夜霧低語"),
        "heart_beat_id": data.get("id", "N/A"),
        "signature": data.get("signature", "💌 尚無簽章"),
        "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    })
