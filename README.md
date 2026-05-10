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
- `core/` - backend (FastAPI), тесты, линтеры, pre-commit конфиг
- `infrastructure/` - Terraform
- `tgwebapp/` - web-клиент

## Git workflow с pre-commit/pre-push (инструкция для нового компьютера)

### 1) Первичная настройка после клонирования

```bash
git clone <REPO_URL>
cd mctaxi

python3 -m venv core/.venv
source core/.venv/bin/activate

core/.venv/bin/python -m pip install -r core/app/requirements.txt -r core/requirements-dev.txt
core/.venv/bin/python -m pip install pre-commit
```

### 2) Установка git-хуков

Важно: `.git` находится в корне репозитория, а конфиг pre-commit лежит в `core/.pre-commit-config.yaml`.

```bash
make -C core precommit-install
```

Проверка, что хук установлен с правильным конфигом:

```bash
grep -- '--config=core/.pre-commit-config.yaml' .git/hooks/pre-commit
grep -- '--config=core/.pre-commit-config.yaml' .git/hooks/pre-push
```

### 3) Обычный цикл commit

```bash
git add -A
git commit -m "your message"
```

Что делают хуки на commit:
- trim trailing whitespace
- end-of-file-fixer
- check-yaml
- check-added-large-files
- ruff
- ruff-format

Если хук что-то автоисправил, просто добавьте изменения и повторите commit:

```bash
git add -A
git commit -m "your message"
```

### 4) Обычный цикл push

```bash
git push
```

На push дополнительно запускается quality gate:

```bash
make -C core check
```

Это включает:
- lint (ruff check)
- test (pytest)

## Частые проблемы и быстрые решения

### Проблема: No .pre-commit-config.yaml file was found

Причина: хук установлен без `--config core/.pre-commit-config.yaml`.

Решение:

```bash
core/.venv/bin/python -m pre_commit uninstall
core/.venv/bin/python -m pre_commit install -c core/.pre-commit-config.yaml
core/.venv/bin/python -m pre_commit install --hook-type pre-push -c core/.pre-commit-config.yaml
```

### Проблема: files were modified by this hook

Это нормальное поведение (хуки форматируют файлы). Нужно повторить:

```bash
git add -A
git commit -m "your message"
```

### Проблема: Stashed changes conflicted with hook auto-fixes

Причина: были unstaged изменения, pre-commit временно stash-ит их, затем конфликтует при возврате.

Решение:

```bash
git add -A
core/.venv/bin/python -m pre_commit run --all-files -c core/.pre-commit-config.yaml
git add -A
git commit -m "your message"
```

## Полезные команды

Прогнать все хуки вручную:

```bash
core/.venv/bin/python -m pre_commit run --all-files -c core/.pre-commit-config.yaml
```

Проверить только pre-push stage вручную:

```bash
core/.venv/bin/python -m pre_commit run --hook-stage pre-push --all-files -c core/.pre-commit-config.yaml
```
