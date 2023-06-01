# {{cookiecutter.project_name}}

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m {{cookiecutter.project_name}}
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "{{cookiecutter.project_name}}"
{{cookiecutter.project_name}}
├── conftest.py  # Fixtures for all tests. 
{%- if cookiecutter.db_info.name != "none" %}
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
{%- endif %}
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "{{cookiecutter.project_name | upper}}_" prefix.

For example if you see in your "{{cookiecutter.project_name}}/settings.py" a variable named like
`random_parameter`, you should provide the "{{cookiecutter.project_name | upper}}_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `{{cookiecutter.project_name}}.settings.Settings.Config`.

An example of .env file:
```bash
{{cookiecutter.project_name | upper}}_RELOAD="True"
{{cookiecutter.project_name | upper}}_PORT="8000"
{{cookiecutter.project_name | upper}}_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

{%- if cookiecutter.otlp_enabled == "True" %}
## OpenTelemetry 

If you want to start your project with OpenTelemetry collector 
you can add `-f ./deploy/docker-compose.otlp.yml` to your docker command.

Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.otlp.yml --project-directory . up
```

This command will start OpenTelemetry collector and jaeger. 
After sending a requests you can see traces in jaeger's UI
at http://localhost:16686/.

This docker configuration is not supposed to be used in production. 
It's only for demo purpose.

You can read more about OpenTelemetry here: https://opentelemetry.io/
{%- endif %}

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/

{%- if cookiecutter.enable_kube == 'True' %}

## Kubernetes
To run your app in kubernetes
just run:
```bash
kubectl apply -f deploy/kube
```

It will create needed components.

If you haven't pushed to docker registry yet, you can build image locally.

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
docker save --output {{cookiecutter.project_name}}.tar {{cookiecutter.project_name}}:latest
```

{%- endif %}
{%- if cookiecutter.enable_migrations == 'True' %}

## Migrations

If you want to migrate your database, you should run following commands:
```bash
{%- if cookiecutter.orm in ['sqlalchemy', 'ormar'] %}
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
{%- elif cookiecutter.orm == 'tortoise' %}
# Upgrade database to the last migration.
aerich upgrade

{%- elif cookiecutter.orm == 'piccolo' %}
# You have to set a PICCOLO_CONF variable
export PICCOLO_CONF="{{cookiecutter.project_name}}.piccolo_conf"
# Now you can easily run migrations using 
piccolo migrations forwards all
{%- endif %}
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
{%- if cookiecutter.orm in ['sqlalchemy', 'ormar'] %}
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
{%- elif cookiecutter.orm == 'tortoise' %}
aerich downgrade
{%- endif %}
```

### Migration generation

To generate migrations you should run:
```bash
{%- if cookiecutter.orm in ['sqlalchemy', 'ormar'] %}
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
{%- elif cookiecutter.orm == 'tortoise' %}
aerich migrate
{%- endif %}
```
{%- endif %}


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

{%- if cookiecutter.db_info.name != "none" %}
{%- if cookiecutter.db_info.name != "sqlite" %}
1. you need to start a database.

I prefer doing it with docker:
```
{%- if cookiecutter.db_info.name == "postgresql" %}
docker run -p "{{cookiecutter.db_info.port}}:{{cookiecutter.db_info.port}}" -e "POSTGRES_PASSWORD={{cookiecutter.project_name}}" -e "POSTGRES_USER={{cookiecutter.project_name}}" -e "POSTGRES_DB={{cookiecutter.project_name}}" {{cookiecutter.db_info.image}}
{%- endif %}
{%- if cookiecutter.db_info.name == "mysql" %}
docker run -p "{{cookiecutter.db_info.port}}:{{cookiecutter.db_info.port}}" -e "MYSQL_PASSWORD={{cookiecutter.project_name}}" -e "MYSQL_USER={{cookiecutter.project_name}}" -e "MYSQL_DATABASE={{cookiecutter.project_name}}" -e ALLOW_EMPTY_PASSWORD=yes {{cookiecutter.db_info.image}}
{%- endif %}
```
{%- endif %}
{%- endif %}


2. Run the pytest.
```bash
pytest -vv .
```
