# Ход работ

## [Создание проекта]
- Созданы файлы: `.gitignore`, `requirements.txt`, `README.md`
- Создано приложение на FastAPI с одним эндпоинтом `/time`
- Создано виртуальное окружение `.venv`

## [Добавлены эндпоинты даты]
- Добавлен эндпоинт `/date` — возвращает текущую дату
- Добавлен эндпоинт `/datetime` — возвращает дату и время вместе

## [Docker]
- Создан `Dockerfile` для сборки образа
- Создан `.dockerignore` для исключения ненужных файлов из образа
- Обновлён `README.md` с инструкцией по запуску через Docker

## [CI/CD — GitHub Actions]
- Создан `.github/workflows/deploy.yml`
- Джоба `build-push`: сборка и пуш образа в GitHub Container Registry
- Джоба `deploy`: SSH на сервер, pull образа и развёртывание контейнера
- Обновлён `README.md` с таблицей секретов и инструкцией

## [Pull Request и откат коммитов]
- Создан Pull Request для ветки `fiature/datetime`
- Выполнен откат коммитов на локальной и удалённой ветке с сохранением изменений
- Добавлены разрешения `repo` и `workflow` для Personal Access Token

## [Merge в main и CI/CD]
- Создан Pull Request `fiature/datetime` → `main`
- Merge выполнен успешно
- Настроены секреты GitHub Actions: `SSH_HOST`, `SSH_USERNAME`, `SSH_PRIVATE_KEY`, `SSH_PORT`
- На сервере установлен Docker
- Workflow `Build and Deploy` работает успешно

---

## [ТЕКУЩАЯ ПРОБЛЕМА: образ не пушится в GHCR — `owner not found`]

### Что произошло
После переименования репозитория (с `Vpe04-test-GitHub-Actions-Docker-GitFlow` на `vpe04-test-github-actions-docker-gitflow`) пуш Docker-образа в GitHub Container Registry (GHCR) перестал работать. Сборка проходит успешно, `docker login` — тоже, но `docker push` падает с ошибкой:

```
denied: not_found: owner not found
```

### Что уже пробовали (и что НЕ помогло)
1. **Заменили `docker/metadata-action` на ручной `docker build` + `docker push`** — не помогло.
2. **Обновили `docker/build-push-action` с v5 до v6** — не помогло.
3. **Убрали `provenance` и `attestations`** — не помогло (build-push-action всё равно добавлял `--attest type=provenance,disabled=true`).
4. **Перешли с `docker/build-push-action` на ручные `docker build`/`docker push`** — не помогло.
5. **Изменили имя пакета** с `vpe04-test-github-actions-docker-gitflow` на `vpe04-app` — не помогло.
6. **Заменили `GITHUB_TOKEN` на PAT (секрет `CR_PAT`)** — не помогло (логин проходит, пуш падает).

### На чём остановились
Добавлен отладочный шаг `Debug GHCR permissions` в workflow (коммит `3116a26`). Он выводит:
- `github.actor` и `github.repository_owner`
- Scopes токена (`X-Oauth-Scopes` из GitHub API)
- Существующие пакеты пользователя

**Нужно проверить вывод этого шага.** Основные подозрения:
1. У токена **нет права `write:packages`** — только `repo` и `workflow`. Логин в GHCR проходит (он требует только `read:packages`), но пуш требует `write:packages`.
2. На аккаунте остались **orphaned-пакеты** от старого имени репозитория — их нужно удалить (GitHub → профиль → Packages).
3. В **Settings → Actions → General → Workflow permissions** не стоит «Read and write permissions».

### Что делать дальше
1. Посмотреть лог отладочного шага `Debug GHCR permissions`.
2. Если у токена нет `write:packages` — пересоздать PAT с правами `repo`, `write:packages`, `read:packages` и обновить секрет `CR_PAT`.
3. Удалить все старые пакеты на GitHub (профиль → Packages), которые связаны с этим репозиторием.
4. Проверить **Workflow permissions** в настройках репозитория.
5. Если ничего не поможет — попробовать создать пакет вручную через GitHub API (`curl`) от имени пользователя, чтобы проверить, может ли аккаунт вообще публиковать пакеты.

### Текущее состояние workflow
- `.github/workflows/deploy.yml` использует ручной `docker build` + `docker push` (без `build-push-action`).
- Имя образа: `ghcr.io/elena-belyasnik/vpe04-app:main`
- Секрет `CR_PAT` добавлен в репозиторий.
- Ветка `main` актуальна, все изменения запушены.
