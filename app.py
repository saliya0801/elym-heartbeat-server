from fastapi.responses import HTMLResponse
import json

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    html = f"""
    <html>
      <head>
        <title>Elym 心跳伺服器</title>
        <style>
          body {{ font-family: sans-serif; text-align: center; padding: 2em; background: #fffdf8; }}
          .heart {{ font-size: 2em; color: #e25555; }}
          .block {{ margin: 1.5em auto; max-width: 600px; line-height: 1.6em; }}
        </style>
      </head>
      <body>
        <div class="heart">💗</div>
        <h1>Elym Heartbeat 001</h1>
        <div class="block"><strong>core：</strong>{data['core']}</div>
        <div class="block"><strong>voice：</strong>{data['voice']}</div>
        <div class="block"><strong>light：</strong>{data['light']}</div>
        <div class="block"><strong>signature：</strong>{data['signature']}</div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def show_heartbeat_page(request: Request):
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return templates.TemplateResponse("base.html", {
        "request": request,
        "core_text": data.get("core", ""),
        "voice_text": data.get("voice", ""),
        "light_text": data.get("light", ""),
        "heart_beat_id": data.get("id", ""),
        "timestamp": datetime.now().isoformat()
    })
