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

## [РЕШЕНО: образ не пушится в GHCR — `owner not found`]

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

### Найденная причина
Логи отладочного шага `Debug GHCR permissions` показали:
- Токен **имеет** `write:packages` и `delete:packages` — с токеном всё в порядке.
- GitHub-логин пользователя: `ElenaBelyasnik` (CamelCase, **без дефиса**).
- В lowercase это `elenabelyasnik`.
- В workflow использовалось `elena-belyasnik` (**с дефисом**) — такого владельца в GHCR не существует → `owner not found`.
- Существующий пакет в GHCR: `vpe04-test-github-actions-docker-gitflow` (orphaned, привязан к старому имени репозитория).

### Что делать дальше
1. ✅ Исправить workflow: заменить `elena-belyasnik` → `elenabelyasnik` везде.
2. ✅ Удалить старый orphaned-пакет `vpe04-test-github-actions-docker-gitflow` на GitHub (профиль → Packages).
3. ✅ Запустить workflow заново и проверить, что пуш проходит.

### Результат
- Коммит `3425b70` запушен в `main`.
- Workflow `Build and Deploy` отработал успешно — обе джобы зелёные.
- Образ `ghcr.io/elenabelyasnik/vpe04-app:main` успешно запушен в GHCR.
- Контейнер развёрнут на сервере.

## [Возврат на GITHUB_TOKEN]
- Убран отладочный шаг `Debug GHCR permissions` — больше не нужен.
- В джобе `build-push`: `CR_PAT` заменён на автоматический `GITHUB_TOKEN`.
- В джобе `deploy`: `CR_PAT` заменён на `GITHUB_TOKEN`.
- Секрет `CR_PAT` больше не используется — можно удалить из настроек репозитория.
- `permissions: packages: write` в `build-push` обеспечивает право на пуш в GHCR.

### Текущее состояние workflow
- `.github/workflows/deploy.yml` использует ручной `docker build` + `docker push` (без `build-push-action`).
- Имя образа: `ghcr.io/elenabelyasnik/vpe04-app:main`
- Для логина в GHCR используется автоматический `GITHUB_TOKEN` (без PAT).
- Ветка `main` актуальна, все изменения запушены.
