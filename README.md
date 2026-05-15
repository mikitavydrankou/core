# mctaxi

Зайти на сервак:
ssh -i ~/.ssh/mctaxi_vm_key nikita@34.107.50.184

Подчистить старые known_hosts
ssh-keygen -f ~/.ssh/known_hosts -R 34.107.50.184

логи почекать
journalctl -u google-startup-scripts.service --no-pager | tail -n 100
tail -n 200 /var/log/startup-script.log


Монорепозиторий проекта с backend, инфраструктурой и web-частью.

Структура:
- `core/` - backend (FastAPI), тесты, линтеры
- `infrastructure/` - Terraform
- `tgwebapp/` - web-клиент
