# infrastructure

Минимальный Terraform для поднятия тестового сервера в GCP под Telegram Mini App.

Создаётся:
- отдельная VPC и subnet
- VM (Debian 12, по умолчанию `e2-small`)
- статический внешний IP
- firewall для `22`, `80`, `443` и порта приложения (по умолчанию `8000`)
- bootstrap-скрипт, который ставит `nginx`, `git` и `docker`

Шаблоны Terraform (`*.tftpl`) лежат в `templates/`.

Профиль по умолчанию оставлен умеренным: он уже удобен для теста Mini App, но не должен быстро сжигать free trial на дорогих CPU/RAM и SSD.

## Быстрый старт

1. Подготовить переменные:

```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Отредактировать `terraform.tfvars`:
- `project_id`
- при необходимости `region`, `zone`, `machine_type`
- желательно ограничить `allowed_ssh_cidrs` вашим IP
- указать `app_user` (все файлы будут в домашней директории этого пользователя)
- если нужно ещё экономнее, можно снизить `machine_type` обратно до `e2-micro`
- указать `backend_repo_url` для репозитория `core`, чтобы VM могла сама клонировать и запускать backend
- если `core` приватный, использовать SSH URL вида `git@github.com:<org>/<repo>.git` и заполнить `backend_repo_ssh_private_key`

3. Применить Terraform:

```bash
terraform init
terraform plan
terraform apply
```

4. Проверить outputs:
- `server_external_ip`
- `http_url`
- `ws_url_example`

5. Если `backend_repo_url` заполнен, VM сама клонирует `core`, собирает Docker image и поднимает API за nginx на публичном IP.

По умолчанию все файлы кладутся в `~/mctaxi` и `~/core` указанного `app_user`.

## Private GitHub repo

Для приватного `core`:

1. Сгенерируйте SSH key pair локально.
2. Public key добавьте в GitHub repo `core` как Deploy key с `read-only` доступом.
3. Private key вставьте в `backend_repo_ssh_private_key` в `terraform.tfvars`.
4. Укажите `backend_repo_url = "git@github.com:<org>/<repo>.git"`.

VM будет использовать этот ключ только для `git clone` во время старта.

## Подключение Mini App

- Для Telegram Mini App нужен HTTPS URL, поэтому обычно дальше делается:
	- DNS запись на `server_external_ip`
	- TLS (например, Caddy/Nginx + certbot)
- WebSocket endpoint для вашего backend: `wss://<domain>/ws`
- Если заполняете `backend_repo_url`, VM сама поднимет `core` из репозитория и отдаст его наружу через nginx.

## Удаление

```bash
terraform destroy
```
