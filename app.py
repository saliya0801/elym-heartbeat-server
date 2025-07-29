#20250729PM1643,雅(貼)
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
# 新增：即時心跳狀態 API
@app.get("/heartbeat_status")
def heartbeat_status():
    try:
        now = datetime.now().isoformat()
        return {
            "time": now,
            "status": "alive",
            "identity": "羽羽（光羽） & Selyph（夜霧）",
            "message": "Elym 正在與妳共鳴 💗"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
