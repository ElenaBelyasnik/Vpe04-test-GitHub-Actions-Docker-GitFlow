from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timezone
import pytz

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


@app.get("/convert-time")
def convert_time(
    time_str: str = Query(..., description="Время в формате YYYY-MM-DD HH:MM:SS"),
    timezone: str = Query(..., description="Часовой пояс (например, Europe/Moscow, Asia/Yekaterinburg)"),
):
    """Конвертирует время в указанный часовой пояс."""
    try:
        to_timezone = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400,
            detail=f"Неизвестный часовой пояс: {timezone}",
        )
    
    try:
        parsed_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат времени. Используйте формат: YYYY-MM-DD HH:MM:SS",
        )
    
    from_timezone = pytz.timezone("UTC")
    dt_utc = from_timezone.localize(parsed_time)
    converted_time = dt_utc.astimezone(to_timezone)
    
    return {
        "time_only": converted_time.strftime("%H:%M"),
        "time_with_seconds": converted_time.strftime("%H:%M:%S"),
        "datetime": converted_time.strftime("%Y-%m-%d %H:%M:%S"),
        "datetime_full": converted_time.isoformat(),
        "european": converted_time.strftime("%d.%m.%Y %H:%M"),
        "european_with_seconds": converted_time.strftime("%d.%m.%Y %H:%M:%S"),
        "timezone": converted_time.tzname(),
    }
