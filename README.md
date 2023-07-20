![python version](https://img.shields.io/pypi/pyversions/fastapi_template?style=for-the-badge) [![version](https://img.shields.io/pypi/v/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)
[![](https://img.shields.io/pypi/dm/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)
<div align="center">
<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/logo.png" width=700>
<div><i>Flexible general-purpose template for FastAPI.</i></div>
</div>

## Usage

⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) must be installed and accessible ⚠️

Poetry version must be greater or equal than 1.1.8. Otherwise it won't be able to install SQLAlchemy.

<div align="center">
 <a href="https://asciinema.org/a/ig0oi0fOq1hxqnW5X49XaaHIT" target="_blank"><img src="https://asciinema.org/a/ig0oi0fOq1hxqnW5X49XaaHIT.svg" /></a>
  <p>Templator in action</p>
</div>

You can install it directly from pypi with pip.
```bash
python3 -m pip install fastapi_template
python3 -m fastapi_template
# or fastapi_template
# Answer all the questions
# 🍪 Enjoy your new project 🍪
cd new_project
docker-compose -f deploy/docker-compose.yml --project-directory . build
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to install it from sources, try this:
```shell
python3 -m pip install poetry
python3 -m pip install .
python3 -m fastapi_template
```

Also, you can use it with docker.
```bash
docker run --rm -it -v "$(pwd):/projects" s3rius/fastapi_template
```

## Features

One of the coolest features is that this project is extremely configurable.
You can choose between different databases and even ORMs, or
you can even generate a project without a database!
Currently SQLAlchemy 2.0, TortoiseORM, Piccolo and Ormar are supported.

This project can run as TUI or CLI and has excellent code documentation.

Generator features:
- Pydantic V2 (Where it's possible. Some libs doesn't have support);
- You can choose between GraphQL and REST api;
- Uvicorn and gunicorn;
- Different databases support;
- Different ORMs support;
- Optional migrations for each ORM except raw drivers;
- Optional redis support;
- Optional rabbitmq support;
- different CI\CD;
- Optional Kubernetes config generation;
- Optional Demo routers and models (This helps you to see how project is structured);
- Pre-commit integration;
- Generated tests with almost 90% coverage;
- Tests for the generator itself;
- Optional Prometheus integration;
- Optional Sentry integration;
- Optional Loguru logger;
- Optional Opentelemetry integration.
- Optional taskiq integration.


This project can handle arguments passed through command line.

```shell
$ python -m fastapi_template --help

Usage: fastapi_template [OPTIONS]

Options:
  -n, --name TEXT                 Name of your awesome project
  -V, --version                   Prints current version
  --force                         Owerrite directory if it exists
  --quite                         Do not ask for features during generation
  --api-type [rest|graphql]       Select API type for your application
  --db [none|sqlite|mysql|postgresql]
                                  Select a database for your app
  --orm [none|ormar|sqlalchemy|tortoise|psycopg|piccolo]
                                  Choose Object–Relational Mapper lib
  --ci [none|gitlab_ci|github]    Select a CI for your app
  --redis                         Add redis support
  --rabbit                        Add RabbitMQ support
  --taskiq                        Add Taskiq support
  --migrations                    Add Migrations
  --kube                          Add kubernetes configs
  --dummy                         Add dummy model
  --routers                       Add example routers
  --swagger                       Add self hosted swagger
  --prometheus                    Add prometheus compatible metrics
  --sentry                        Add sentry integration
  --loguru                        Add loguru logger
  --opentelemetry                 Add opentelemetry integration
  --traefik                       Adds traefik labels to docker container
  --kafka                         Add Kafka support
  --gunicorn                      Add gunicorn server
  --help                          Show this message and exit.
```
