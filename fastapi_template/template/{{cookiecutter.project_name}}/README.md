# {{cookiecutter.project_name}}

Start a project with:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up
```

## Pre-commit

To install pre-commit simply run inside of the shell:
```bash
pre-commit install
```
{%- if cookiecutter.enable_kube == 'True' %}

## Kubernetes
To run your app in kubernetes
just run:
```bash
kubectl apply -f deploy/kube
```

It will create needed components.

If you hasn't pushed to docker registry yet, you can build image locally.

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
docker save --output {{cookiecutter.project_name}}.tar {{cookiecutter.project_name}}:latest
```

{%- endif %}
{%- if cookiecutter.enable_migrations == 'True' %}

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations untill the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Miration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

{%- endif %}


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
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
