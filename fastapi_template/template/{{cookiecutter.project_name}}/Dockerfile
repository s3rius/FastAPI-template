FROM python:3.11.4-slim-bullseye as prod

{%- if cookiecutter.db_info.name == "mysql" %}
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}


{%- if cookiecutter.db_info.name == "postgresql" %}
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}


RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main

{%- if cookiecutter.db_info.name == "mysql" or cookiecutter.db_info.name == "postgresql" %}
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

CMD ["/usr/local/bin/python", "-m", "{{cookiecutter.project_name}}"]

FROM prod as dev

RUN poetry install
