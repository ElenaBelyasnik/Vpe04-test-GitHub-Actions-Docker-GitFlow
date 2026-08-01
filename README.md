# FastAPI — Тестовый бэкенд

## Описание
Простое тестовое приложение на FastAPI, возвращающее текущее время сервера.

## Запуск

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```

 4. Откройте в браузере:
    - [http://127.0.0.1:8000/time](http://127.0.0.1:8000/time)
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Swagger UI

## Запуск через Docker

1. Соберите образ:
   ```bash
   docker build -t fastapi-app .
   ```

2. Запустите контейнер:
   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

3. Откройте в браузере:
   - [http://127.0.0.1:8000/time](http://127.0.0.1:8000/time)
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Swagger UI
