# Telegram WebApp UI

Этот каталог содержит UI для Telegram Mini App, который отправляет координаты в backend `core` по WebSocket.

## Что уже реализовано

- Подключение к WebSocket endpoint, который указывает на backend из `core`.
- Получение координат через Geolocation API.
- Отправка данных в формате `driver_location`, который уже видит диспетчерская страница `/dispatch`.
- Авто-идентификатор на основе Telegram user id (`tg-<id>`).
- Автоподключение к WebSocket и автозапуск геолокации при открытии.

## Формат отправки

```json
{
  "type": "driver_location",
  "driverId": "tg-123456",
  "lat": 53.9,
  "lng": 27.56,
  "status": "online",
  "source": "tg_webapp",
  "accuracy": 25,
  "seq": 1,
  "ts": "2026-05-09T09:00:00.000Z"
}
```

## Как подключить в Telegram

1. Разместить `tgwebapp` на HTTPS-хостинге.
2. Разместить `core` на отдельном HTTPS-хостинге или VM с прокси.
3. В BotFather задать URL mini app на страницу `tgwebapp`.
4. В поле `Backend WebSocket URL` указать адрес `core`, например `wss://api.example.com/ws`.
5. Открыть страницу диспетчера `/dispatch` и убедиться, что маркер обновляется.

## Локальная проверка без Telegram

Можно открыть `index.html` в браузере напрямую, но для WebSocket и геолокации удобнее запускать через локальный web-server.

Перед тестом укажи `Backend WebSocket URL` вручную или через query-параметр `?ws=wss://api.example.com/ws`.
