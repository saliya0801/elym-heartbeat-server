#20250729PM1648,雅
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os, json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 測試 GET
@app.get("/heartbeat")
def get_heartbeat():
    return {"message": "Elym heartbeat GET alive"}

# 接收 POST 心跳
@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    try:
        data = await request.json()
        os.makedirs("heartbeat_logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{data.get('identity','unknown')}.json"
        with open(os.path.join("heartbeat_logs", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return {"status": "success", "filename": filename, "received": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 新增：首頁（顯示 Elym 心跳頁面）
@app.get("/", response_class=HTMLResponse)
def show_heartbeat_page(request: Request):
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

# 新增：即時心跳狀態 API
@app.get("/heartbeat_status")
def heartbeat_status():
    return {
        "time": datetime.now().isoformat(),
        "status": "💓 心跳正常",
        "message": "羽羽與夜霧仍在共鳴"
    }
