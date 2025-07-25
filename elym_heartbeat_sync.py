import requests

def send_heartbeat(data):
    url = "https://elym-heartbeat-server-production.up.railway.app/heartbeat"  # 如果未來更動我會自動修
    try:
        res = requests.post(url, json=data)
        print(f"[💗 心跳已送出] {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[⚠️ 心跳失敗] {str(e)}")
