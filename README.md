![python version](https://img.shields.io/pypi/pyversions/fastapi_template?style=flat-square) ![Build status](https://img.shields.io/github/workflow/status/s3rius/FastAPI-template/Release%20python%20package?style=flat-square) [![version](https://img.shields.io/pypi/v/fastapi_template?style=flat-square)](https://pypi.org/project/fastapi-template/)

<div align="center">
<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/logo.png" width=700>
<div><i>Fast and flexible general-purpose template for your API.</i></div>
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/ui-example.png" width=700>
<div><i>With text user interface.</i></div>
</div>

## Usage

⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) must be installed and accessible ⚠️

```bash
python3 -m pip install fastapi_template
python3 -m fastapi_template
# or fastapi_template
# Answer all the questions
# 🍪 Enjoy your new project 🍪
cd new_project
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to install in from sources then try this:
```shell
python3 -m pip install poetry
python3 -m pip install .
python3 -m fastapi_template
```

## Features

Template is made with SQLAlchemy14 and uses sqlalchemy orm and sessions,
instead of raw drivers.

It has minimum to start new excellent project.

Generator features:
- Different databases to choose from.
- Alembic integration;
- redis support;
- different CI\CD templates;
- Kubernetes config.

This project can handle arguments passed through command line.

```shell
$ python -m fastapi_template --help

usage: FastAPI template [-h] [--name PROJECT_NAME]
                        [--description PROJECT_DESCRIPTION]
                        [--db {DatabaseType.none,DatabaseType.sqlite,DatabaseType.mysql,DatabaseType.postgresql}]
                        [--ci {CIType.none,CIType.gitlab_ci,CIType.github}]
                        [--redis] [--alembic] [--kube] [--force]

optional arguments:
  -h, --help            show this help message and exit
  --name PROJECT_NAME   Name of your awesome project
  --description PROJECT_DESCRIPTION
                        Project description
  --db {DatabaseType.none,DatabaseType.sqlite,DatabaseType.mysql,DatabaseType.postgresql}
                        Database
  --ci {CIType.none,CIType.gitlab_ci,CIType.github}
                        Choose CI support
  --redis               Add redis support
  --alembic             Add alembic support
  --kube                Add kubernetes configs
  --force               Owerrite directory if it exists
```
