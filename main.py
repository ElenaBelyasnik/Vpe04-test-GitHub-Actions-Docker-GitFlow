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


@app.get("/date")
def get_date():
    """Возвращает текущую дату сервера."""
    now = datetime.now(timezone.utc)
    return {
        "server_date": now.date().isoformat(),
        "timezone": "UTC",
    }


@app.get("/datetime")
def get_datetime():
    """Возвращает текущие дату и время сервера."""
    now = datetime.now(timezone.utc)
    return {
        "server_datetime": now.isoformat(),
        "server_date": now.date().isoformat(),
        "server_time": now.time().isoformat(),
        "timezone": "UTC",
    }
