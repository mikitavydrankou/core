# core

## Архитектура и правила

Структура приложения и правила развития описаны в [app/README.md](app/README.md).

## WebSocket monitor

После запуска backend откройте [http://127.0.0.1:8000/monitor](http://127.0.0.1:8000/monitor), чтобы видеть все сообщения, приходящие по WebSocket на `/ws`.

## Minimal map flow

- [http://127.0.0.1:8000/sim](http://127.0.0.1:8000/sim) - multi-driver simulator that moves several fake drivers and sends their coordinates.
- [http://127.0.0.1:8000/dispatch](http://127.0.0.1:8000/dispatch) - dispatcher map with live driver markers.

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

### CI

В репозитории добавлен workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml), который запускает `make check` на каждый push и pull request.

Если backend запущен через Docker, пересоберите контейнер после изменений:

```bash
docker compose up -d --build
```