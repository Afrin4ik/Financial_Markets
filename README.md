# Financial Markets

## Настройка (с помощью uv)

В этом проекте файл `pyproject.toml` используется в качестве основного источника информации о зависимостях

### 1. Установка uv

```bash
brew install uv
```

### 2. Создание виртуального окружения и его активация

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Установка всех зависимостей

```bash
uv sync
```

Пакет `tinkoff-investments` устанавливается из официального репозитория Git
с закреплённого тега, а неработающая транзитивная зависимость `tinkoff` исключается с помощью
конфигурации `[tool.uv]` в файле `pyproject.toml`

## Запуск API

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Открыть:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs