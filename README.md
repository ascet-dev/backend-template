# Архитектура приложения на основе adc-appkit и adc-webkit

## Обзор

Проект построен на основе современных Python-фреймворков `adc-appkit` и `adc-webkit`, которые обеспечивают управление жизненным циклом компонентов, dependency injection и веб-API.

## Ключевые особенности

### 1. Управление жизненным циклом

- **Автоматическая инициализация** компонентов при запуске приложения через `BaseApp`
- **Корректное завершение** работы всех компонентов при остановке через `_stop()` метод
- **Управление состояниями** компонентов через методы `is_alive()` и health checks

### 2. Компонентная архитектура

- **PG компонент** - подключение к PostgreSQL с пулом соединений
- **S3 компонент** - работа с объектным хранилищем (MinIO)
- **Web компонент** - REST API с автоматической документацией OpenAPI
- **DAO компонент** - слой доступа к данным через SQLAlchemy

### 3. Управление зависимостями

- **Dependency injection** через декоратор `@component`
- **Автоматическое разрешение зависимостей** между компонентами
- **Конфигурация через Pydantic** с поддержкой переменных окружения

### 4. Мониторинг и отладка

- **Health checks** через endpoints `/readiness` и `/liveness`
- **Проверка состояния** всех компонентов (PG, S3, HTTP)
- **Логирование** через структурированные логи с Sentry интеграцией

## Структура файлов

```
back_template/
├── services/
│   ├── __init__.py          # Экспорт App класса
│   ├── service.py           # Основной App класс с компонентами
│   ├── repositories.py       # DAO слой для работы с БД
│   └── schemas.py           # Pydantic схемы
├── web/
│   ├── __init__.py          # Веб модуль
│   ├── app.py              # WebApp конфигурация
│   ├── endpoints.py        # REST API endpoints
│   └── auth.py             # Аутентификация
├── settings/
│   ├── __init__.py          # Экспорт cfg
│   ├── settings.py          # Основная конфигурация
│   ├── app.py              # Настройки приложения
│   ├── postgres.py         # Настройки PostgreSQL
│   ├── s3.py               # Настройки S3/MinIO
│   ├── auth.py             # Настройки JWT
│   └── logs.py             # Настройки логирования
├── models/
│   ├── __init__.py          # Экспорт моделей
│   └── base.py              # Базовые модели SQLAlchemy
├── manage.py               # CLI для управления приложением
├── docker-compose.yml      # Docker окружение
└── pyproject.toml          # Зависимости проекта
```

## Основные классы

### 1. App (BaseApp)

Основной класс приложения, наследующий от `BaseApp` из `adc-appkit`:

```python
class App(BaseApp):
    pg = component(PG, config_key="pg")

    @property
    def dao(self) -> DAO:
        if not hasattr(self, "_dao"):
            if not self.pg.is_alive():
                raise RuntimeError("PG is not alive")
            self._dao = DAO(self.pg)
        return self._dao

    async def _stop(self):
        pass

    async def business_logic(self):
        return await self.dao.pm.fetch("SELECT 1")
```

### 2. WebApp (Web)

Веб-приложение на основе `adc-webkit`:

```python
class WebApp(Web):
    cors = cfg.app.cors.model_dump()
    routes = [
        Route("GET", "/readiness", Readiness),
        Route("GET", "/liveness", Liveness),
    ]

web = WebApp.create(bindings={'app': app})
```

### 3. DAO (PostgresAccessLayer)

Слой доступа к данным:

```python
class DAO(PostgresAccessLayer, metadata=m.base.meta):
    pass
```

### 4. Endpoints

REST API endpoints с автоматической документацией:

```python
class Readiness(JsonEndpoint):
    doc = Doc(tags=["default"], summary="check if the server is ready")
    response = Response(ReadinessResponse)

    async def execute(self, _) -> dict:
        components = list(ReadinessResponse.__annotations__)
        statuses = await asyncio.gather(*(getattr(self.web.state.app, com).is_alive() for com in components))
        return dict(zip(components, statuses, strict=True))
```

## Примеры использования

### Запуск приложения

```bash
# Запуск веб-сервера
python manage.py start-web

# Применение SQL скрипта
python manage.py apply-sql data.sql
```

### Работа с компонентами

```python
# Получение DAO для работы с БД
dao = app.dao
result = await dao.pm.fetch("SELECT * FROM users")

# Проверка состояния компонентов
pg_alive = app.pg.is_alive()
```

### Создание новых endpoints

```python
class UserEndpoint(JsonEndpoint):
    doc = Doc(tags=["users"], summary="Get user by ID")
    response = Response(UserResponse)

    async def execute(self, user_id: str) -> dict:
        dao = self.web.state.app.dao
        user = await dao.pm.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return {"user": user}
```

### Конфигурация через переменные окружения

```bash
# PostgreSQL
PG__CONNECTION__DSN=postgresql://user:pass@localhost:5432/db
PG__CONNECTION__MAX_SIZE=10

# S3/MinIO
S3__CONNECTION__URL=http://localhost:9000
S3__CONNECTION__ACCESS_KEY=minioadmin
S3__CONNECTION__SECRET_KEY=minioadmin

# Приложение
APP__HOST=0.0.0.0
APP__PORT=8001
```

## Преимущества архитектуры

1. **Готовые компоненты** - использование проверенных библиотек `adc-appkit` и `adc-webkit`
2. **Автоматическое управление жизненным циклом** - компоненты инициализируются и завершаются автоматически
3. **Dependency injection** - простое внедрение зависимостей через декораторы
4. **Автоматическая документация** - OpenAPI документация генерируется автоматически
5. **Health checks** - встроенные проверки состояния всех компонентов
6. **Конфигурация через Pydantic** - типизированная конфигурация с валидацией
7. **Docker-ready** - готовое окружение для разработки и продакшена
8. **Структурированное логирование** - интеграция с Sentry для мониторинга
9. **Асинхронность** - полная поддержка async/await
10. **Типизация** - полная поддержка type hints с mypy

## Тестирование

Проект настроен для комплексного тестирования:

- **pytest** - основной фреймворк для тестирования
- **pytest-asyncio** - поддержка асинхронных тестов
- **pytest-cov** - покрытие кода тестами
- **pytest-mock** - мокирование компонентов
- **pytest-xdist** - параллельное выполнение тестов

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=services --cov=web --cov=settings

# Параллельно
pytest -n auto

# Только unit тесты
pytest -m unit
```

## Разработка

### Инструменты разработки

- **black** - форматирование кода
- **isort** - сортировка импортов
- **ruff** - линтер и форматтер
- **mypy** - проверка типов
- **pre-commit** - хуки для git
- **bandit** - проверка безопасности

### Docker окружение

```bash
# Запуск всех сервисов
docker-compose up -d

# Только база данных
docker-compose up postgres -d

# Миграции
docker-compose up postgres_migrations

# Применение данных
docker-compose up data_migrations
```

## Заключение

Данная архитектура предоставляет:

- **Современный стек** на основе `adc-appkit` и `adc-webkit`
- **Готовое решение** для быстрого старта разработки
- **Автоматическое управление** жизненным циклом компонентов
- **Встроенные инструменты** для разработки и тестирования
- **Docker-окружение** для локальной разработки
- **Полную типизацию** и проверку качества кода
- **Готовую документацию** API через OpenAPI

Архитектура готова к использованию в реальных проектах и может быть легко расширена под конкретные требования бизнеса.
