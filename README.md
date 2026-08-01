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
    - [http://127.0.0.1:8000/date](http://127.0.0.1:8000/date)
    - [http://127.0.0.1:8000/datetime](http://127.0.0.1:8000/datetime)
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

## CI/CD — GitHub Actions

Workflow настроен в `.github/workflows/deploy.yml`. Он состоит из двух джоб:

1. **build-push** — собирает Docker-образ и пушит его в GitHub Container Registry.
2. **deploy** — подключается к серверу по SSH, скачивает образ и разворачивает контейнер.

### Необходимые секреты репозитория

Настройте в **Settings → Secrets and variables → Actions**:

| Секрет | Описание |
|---|---|
| `GITHUB_TOKEN` | Создаётся автоматически, используется для логина в GHCR |
| `SSH_HOST` | IP-адрес или домен сервера |
| `SSH_USERNAME` | Имя пользователя для SSH |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ (формат `-----BEGIN OPENSSH PRIVATE KEY-----`) |
| `SSH_PORT` | Порт SSH (по умолчанию `22`) |

### Ручной запуск

Можно запустить workflow через **Actions → "Build and Deploy" → Run workflow**.
