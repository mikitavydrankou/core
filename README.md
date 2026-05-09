# core

## WebSocket monitor

После запуска backend откройте [http://127.0.0.1:8000/monitor](http://127.0.0.1:8000/monitor), чтобы видеть все сообщения, приходящие по WebSocket на `/ws`.

Если backend запущен через Docker, пересоберите контейнер после изменений:

```bash
docker compose up -d --build
```