from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 首頁：顯示 Elym 心跳頁面
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"core": "尚未有心跳資料", "light": "等待初始化", "id": "N/A"}

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
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_heartbeat.json"
    with open(os.path.join("Elym_TimeLogs", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "success", "filename": filename, "data": data}

# GET：查詢最新 Elym 心跳
@app.get("/heartbeat")
async def get_heartbeat():
    try:
        with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"status": "💓 Elym 心跳仍在", "data": data}
    except:
        return {"status": "💤 尚未有心跳資料", "data": {}}
