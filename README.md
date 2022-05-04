![python version](https://img.shields.io/pypi/pyversions/fastapi_template?style=for-the-badge) ![Build status](https://img.shields.io/github/workflow/status/s3rius/FastAPI-template/Release%20python%20package?style=for-the-badge) [![version](https://img.shields.io/pypi/v/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)
[![](https://img.shields.io/pypi/dm/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)
<div align="center">
<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/logo.png" width=700>
<div><i>Flexible and Lightweight general-purpose template for FastAPI.</i></div>
</div>

## Usage

⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) must be installed and accessible ⚠️

Poetry version must be greater or equal than 1.1.8. Otherwise it won't be able to install SQLAlchemy.

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

If you want to install in from sources then try this:
```shell
python3 -m pip install poetry
python3 -m pip install .
python3 -m fastapi_template
```

Also you can use it with docker.
```bash
docker run --rm -it -v "$(pwd):/projects" s3rius/fastapi_template
```

<div align="center">
  <img src="https://user-images.githubusercontent.com/18153319/137182689-ce714440-7576-46a0-8f96-862a8469a28c.gif"/>
  <p>Templator in action</p>
</div>


## Features

One of the coolest features is that this project is extremely small and handy.
You can choose between different databases and even ORMs. 
Currently SQLAlchemy1.4, TortoiseORM and Ormar are supported.

TUI and CLI and excellent code documentation.

Generator features:
- You can choose between GraphQL and REST api;
- Different databases support;
- Different ORMs support;
- Optional migrations for each ORM except raw drivers;
- redis support;
- rabbitmq support;
- different CI\CD;
- Kubernetes config generation;
- Demo routers and models;
- Pre-commit integrations;
- Generated tests;
- Tests for the generator itself.

This project can handle arguments passed through command line.

```shell
$ python -m fastapi_template --help

usage: FastAPI template [-h] [--version] [--name PROJECT_NAME]
                        [--description PROJECT_DESCRIPTION]
                        [--api-type {rest,graphql}]
                        [--db {none,sqlite,mysql,postgresql}]
                        [--orm {ormar,sqlalchemy,tortoise,psycopg,piccolo}]
                        [--ci {none,gitlab_ci,github}] [--redis] [--rabbit]
                        [--migrations] [--kube] [--dummy] [--routers]
                        [--swagger] [--force] [--quite]

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         Prints current version
  --name PROJECT_NAME   Name of your awesome project
  --description PROJECT_DESCRIPTION
                        Project description
  --api-type {rest,graphql}
                        API type
  --db {none,sqlite,mysql,postgresql}
                        Database
  --orm {ormar,sqlalchemy,tortoise,psycopg,piccolo}
                        ORM
  --ci {none,gitlab_ci,github}
                        Choose CI support
  --redis               Add Redis support
  --rabbit              Add RabbitMQ support
  --migrations          Add migrations support
  --kube                Add Kubernetes configs
  --dummy, --dummy-model
                        Add dummy model
  --routers             Add example routers
  --swagger             Enable self-hosted Swagger
  --force               Owerrite directory if it exists
  --quite               Do not ask for features during generation
```
