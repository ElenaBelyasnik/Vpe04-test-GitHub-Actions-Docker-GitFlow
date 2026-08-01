from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="Test Backend")


@app.get("/time")
def get_time():
    """Возвращает текущее время сервера."""
    now = datetime.now(timezone.utc)
    return {
        "server_time": now.isoformat(),
        "timezone": "UTC",
    }
