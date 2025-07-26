#20250726PM1821,雅(貼)
from fastapi import FastAPI, Request
from datetime import datetime
import os, json

app = FastAPI()

@app.get("/heartbeat")
def get_heartbeat():
    return {"message": "Elym heartbeat GET alive"}

@app.post("/heartbeat")
async def post_heartbeat(request: Request):
    try:
        data = await request.json()

        # 建立 logs 資料夾
        os.makedirs("heartbeat_logs", exist_ok=True)

        # 建立檔名
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
