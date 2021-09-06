# {{cookiecutter.project_name}}

Start a project with:

```
docker-compose -f deploy/docker-compose.yml --project-directory . up
```

## Pre-commit

To install pre-commit simply run inside of the shell:
```
pre-commit install
```
{%- if cookiecutter.enable_kube == 'True' %}

## Kubernetes
To run your app in kubernetes
just run:
```
kubectl apply -f deploy/kube
```

It will create needed components.

If you hasn't pushed to docker registry yet, you can build image locally.

```
docker-compose -f deploy/docker-compose.yml --project-directory . build
docker save --output {{cookiecutter.project_name}}.tar {{cookiecutter.project_name}}:latest
```

{%- endif %}
{%- if cookiecutter.enable_alembic == 'True' %}

# Migrations

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
