from flask import Flask, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates")

@app.route("/heartbeat")
def heartbeat():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return app.response_class(
        response=json.dumps(data, ensure_ascii=False, indent=2),
        status=200,
        mimetype='application/json'
    )

@app.route("/")
def render():
    with open("heart_beat_memory.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["timestamp"] = datetime.utcnow().isoformat()
    return render_template(
        "base.html",
        core_text=data["core"],
        light_text=data["light"],
        heartbeat_id=data["id"],
        timestamp=data["timestamp"]
    )

if __name__ == "__main__":
    app.run(debug=True)
