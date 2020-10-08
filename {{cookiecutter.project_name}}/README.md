# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Для разработчиков

Для локального запуска достаточно выполнить команду "docker-compose up"

### Требуемые переменные среды для CI\CD
* APP_DIR - путь до проекта на сервере
* ENV_FILE_PATH - путь до файла с переменными среды

## Инсутрукция по развертыванию системы

Сначала потребуется установить все зависимости

Это можно сделать как с помощью poetry, так и с помощью pip
```bash
poetry install
```

```bash
python -m pip install -r requirements.txt
```

Для запуска или проведения тестирования потребуется выставить нужные переменные среды.
Пример переменных среды можно найти в файле `.env.example`.

Если новые параметры запуска хранятся в .env файле, то запуск тестов/системы лучше производить через dotenv или указать `EnvironmentFile` в конфигурации systemd-модуля.

### Применение миграций
Перед запуском системы важно не забыть применить миграции. Для этого, находясь в папке с приложением
следует выполнить следующую команду:
```bash
dotenv -f ".env.file" run alembic upgrade head;
```

Для запуска через dotenv:
```bash
# Запуск тестирования
dotenv -f envs/test.env run pytest
# Запуск системы
dotenv -f envs/test.env run uvicorn --access-log --log-level debug --host 0.0.0.0 --port 8100 src.server:app
```

Для запуска с выставленными переменными среды:
```bash
# Запуск тестов
pytest
# Запуск приложения
uvicorn --access-log --log-level debug --host 0.0.0.0 --port 8100 src.server:app
```

Пример сконфигурированного systemd-модуля представлен в файле [systemd/{{cookiecutter.project_name}}_service.service](systemd/{{ cookiecutter.project_name }}_service.service)


## Запуск планировщика задач
Планировщик сделан чтобы некоторые задачи могли выполнятся на фоне системы.

```bash
# Для запуска с выставленными переменными среды:
python scheduler.py
 
# Для запуска через dotenv
dotenv -f envs/.env run python scheduler.py
```

Пример сконфигурированного systemd-модуля представлен в файле [systemd/{{cookiecutter.project_name}}_scheduler.service](systemd/{{ cookiecutter.project_name }}_scheduler.service)

## Немного про systemd файлы

Для применения на другой машине, скорее всего потребуется поменять следующие параметры в файле:
* EnvironmentFile - файл с описанием переменных среды (Полный путь до файла в системе);
* WorkingDirectory путь до папки с проектом;
* ExecStart - команда запуска приложения.