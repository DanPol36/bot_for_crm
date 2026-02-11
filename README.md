# CRM Telegram Bot + Web UI

English: A simple CRM Telegram bot to view, import and export clients, with a small web UI and Postgres integration.

Русский: Простой Telegram-бот для CRM — просмотр, импорт и экспорт клиентов, небольшой веб‑интерфейс и интеграция с Postgres.

Цель репозитория: показать работу с Telegram Bot API, базой данных Postgres и импортом данных.

## Что в проекте
- `bot/` — Telegram-бот на `aiogram` (экспорт клиентов, импорт из CSV/XLSX, простая авторизация).
- `db_client.py` — утилиты для прямого доступа к Postgres через SQLAlchemy.

## Подготовка (локально)
1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

3. Создайте файл переменных окружения (пример `bot/.env`):

```bash
cp .env.example bot/.env
# затем отредактируйте bot/.env, НЕ добавляйте реальные токены в репозиторий
```

4. Запустите веб‑сервис (если он нужен локально) и бота:

```bash
# пример запуска (зависит от web app реализации)
python bot.py

# в другой консоли
python bot/bot.py
```

## Docker
В репозитории есть `Dockerfile` и `docker-compose.yml` для удобного деплоя/демо.

```bash
docker-compose up --build
```

## The purpose of the repository is to demonstrate how to work with the Telegram Bot API, the Postgres database, and data import.

## What's in the project
- `bot/` - Telegram bot on `aiogram` (export of clients, import from CSV/XLSX, and simple authorization).
- `db_client.py` - utilities for direct access to Postgres via SQLAlchemy.

## Preparation (locally)
1. Clone the repository.
2. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate # Linux/macOS
.\.venv\Scripts\activate # Windows PowerShell
pip install -r requirements.txt
```

3. Create an environment variable file (example `bot/.env`):

```bash
cp .env.example bot/.env
# then edit bot/.env, DO NOT add real tokens to the repository
```

4. Start the web service (if you need it locally) and the bot:

```bash
# example of starting (depends on the web app implementation)
python bot.py

# in another console
python bot/bot.py
```

## Docker
The repository has a `Dockerfile` and `docker-compose.yml` for convenient deployment/demo.
docker-compose up --build
