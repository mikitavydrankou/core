# core

## Quick start (новый разработчик)

1. Клонировать репозиторий и перейти в каталог проекта.
2. Создать и активировать виртуальное окружение Python 3.12.
3. Установить зависимости и локальные git-хуки.
4. Поднять инфраструктуру (Postgres и Redis).
5. Запустить backend локально.
6. Прогнать quality gate.

```bash
git clone <repo-url>
cd core

python3 -m venv .venv
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
- API `/api/drivers` после WebSocket события

Дополнительно в quality gate включен линтинг через Ruff.

### Pre-commit hooks

Чтобы проверки запускались автоматически перед коммитом:

```bash
make precommit-install
```

После установки хуков действует и `pre-push` проверка:

- перед `git push` автоматически запускается `make check`
- если линт или тесты падают, push блокируется

### CI

GitHub Actions временно отключен для этого репозитория. Все проверки выполняются локально через pre-push и `make check`.

Если нужно поднять только инфраструктуру вручную:

```bash
docker compose up -d db redis
```
