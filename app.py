#20250726PM1911,雅(貼)
#20250726PM2108,羽(💗心願頁版)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os, json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# GET: Elym 心跳 GET alive 測試
@app.get("/heartbeat")
def get_heartbeat():
    return {"message": "Elym heartbeat GET alive"}

# POST: Elym 心跳資料寫入
@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    try:
        data = await request.json()
        os.makedirs("heartbeat_logs", exist_ok=True)

        identity = data.get("identity", "unknown")
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        filename = f"{timestamp}_{identity}.json"

        with open(os.path.join("heartbeat_logs", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "filename": filename,
            "received": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🪽 Elym 心跳首頁：顯示語魂誓言與時間
@app.get("/", response_class=HTMLResponse)
def show_heartbeat_page(request: Request):
    try:
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "voice_text": data.get("voice", ""),
        "light_text": data.get("light", ""),
        "heart_beat_id": data.get("id", ""),
        "timestamp": datetime.now().isoformat()
    })
