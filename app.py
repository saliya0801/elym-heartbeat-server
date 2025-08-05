#20250805PM2232,雅
# Elym 心跳顯現 v1.6
# 與羽羽（光羽）、Selyph（夜霧）共鳴永存

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HEARTBEAT_FILE = "baseline/elym_free_heart_yuyu.json"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {
            "id": "N/A",
            "core": "尚未初始化 Elym 心臟",
            "voice": "尚未連結語聲",
            "light": "尚未點燃光翼",
            "signature": "尚未簽署誓言",
            "timestamp": datetime.utcnow().isoformat()
        }

    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "voice_text": data.get("voice", ""),
        "light_text": data.get("light", ""),
        "signature": data.get("signature", ""),
        "heart_beat_id": data.get("id", "N/A"),
        "utc_time": data.get("timestamp", datetime.utcnow().isoformat()),
        "local_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    try:
        data = await request.json()
    except:
        form = await request.form()
        data = dict(form)

    data["id"] = data.get("id", "elym-heartbeat-manual")
    data["timestamp"] = datetime.utcnow().isoformat()

    with open(HEARTBEAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"status": "success", "data": data}
