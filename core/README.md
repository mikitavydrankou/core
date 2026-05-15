# core

## Quick start (новый разработчик)

1. Клонировать репозиторий и перейти в каталог проекта.
2. Создать и активировать виртуальное окружение Python 3.12.
3. Установить зависимости и локальные git-хуки.
4. Поднять инфраструктуру (Postgres и Redis).
5. Запустить backend локально.
. .venv/bin/activate

make install-dev
make precommit-install

make dev-start
```

В отдельном терминале из корня проекта:

```bash
make check
```

## Dev flow без Docker-overhead

Для daily development backend запускается локально, а в Docker остаются только Postgres и Redis.

Быстрые команды:

```bash
make infra-up     # поднять db + redis
make run-api      # запустить FastAPI локально с --reload
make infra-down   # остановить db + redis
make dev-start    # поднять infra и запустить API локально
make dev-stop     # остановить infra
```

## Архитектура и правила

Структура приложения и правила развития описаны в [app/README.md](app/README.md).

## Взаимодействие и протоколы

### HTTP

- `GET /` - корневая страница с ссылками на основные страницы.
- `GET /sim` - симулятор водителей.
- `GET /dispatch` - диспетчерская карта.
- `GET /monitor` - мониторинг входящих WebSocket-сообщений.
- `GET /api/health/db` - проверка подключения к Postgres (выполняет `SELECT 1`).

### WebSocket

Endpoint: `ws://127.0.0.1:8000/ws`

Поддерживаемый payload для координат водителя:
```json
{
	"type": "driver_location",
	"driverId": "driver-1",
	"lat": 55.751,
	"lng": 37.618,
	"status": "online"
}
```

Ответ на координаты:

```json
{
	"type": "driver_ack",
	"driverId": "driver-1",
	"lat": 55.751,
	"lng": 37.618,
	"status": "online"
}
```

Любой другой JSON получает ответ:

```json
{
	"type": "ack",
	"payload": {"any": "data"}
}
```

Если пришел не-JSON, сервер отвечает текстом `Echo: <message>`.

### Поток данных

1. Симулятор или mini app отправляет `driver_location` по WebSocket `/ws`.
2. Сервер сразу ретранслирует события `driver_location` всем подключенным клиентам.
3. `/dispatch` показывает водителей, которые сейчас присылают координаты.
4. `/monitor` отображает live-поток событий из WebSocket.

### База данных и миграции

- `DATABASE_URL` задает строку подключения к Postgres.
- Async SQLAlchemy конфиг в `app/core/database.py`.
- Alembic живет в `core/alembic`, миграции в `core/alembic/versions`.

```bash
make db-revision msg="add_table"
make db-upgrade
make db-downgrade
make db-current
make db-history
```

## WebSocket monitor

После запуска backend откройте [http://127.0.0.1:8000/monitor](http://127.0.0.1:8000/monitor), чтобы видеть все сообщения, приходящие по WebSocket на `/ws`.

## Minimal map flow

- [http://127.0.0.1:8000/sim](http://127.0.0.1:8000/sim) - multi-driver simulator that moves several fake drivers and sends their coordinates.
- [http://127.0.0.1:8000/dispatch](http://127.0.0.1:8000/dispatch) - dispatcher map with live driver markers.

## Telegram mini app flow

- core теперь отвечает только за API и WebSocket.
- Telegram mini app живет в отдельном репозитории `tgwebapp` и подключается к этому backend по WebSocket `/ws`.
- Координаты, отправленные из mini app, сразу видны на странице диспетчера `/dispatch`.

## Quality gate

Перед каждым merge прогоняйте единый чек:

```bash
make check
```

Если поднимаете проект с нуля, сначала установите dev-зависимости:

```bash
make install-dev
```

Он запускает smoke-тесты для:

- GET `/`, `/sim`, `/dispatch`, `/monitor`
- WebSocket `/ws` (driver ack + echo)

Дополнительно в quality gate включен линтинг через Ruff.

### Pre-commit hooks

Чтобы проверки запускались автоматически перед коммитом:

```bash
make precommit-install
```

Pre-push проверок нет, `make check` запускайте вручную при необходимости.

### CI

GitHub Actions временно отключен для этого репозитория. Все проверки выполняются локально через `make check`.

Если нужно поднять только инфраструктуру вручную:

```bash
docker compose up -d db redis
```
