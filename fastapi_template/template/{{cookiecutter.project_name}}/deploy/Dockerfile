FROM python:3.9.6-slim-buster

{% if cookiecutter.db_info.name == "mysql" -%}
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}

RUN pip install poetry==1.1.8

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install

{%- if cookiecutter.db_info.name == "mysql" %}
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}

# Copying actuall application
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "{{cookiecutter.project_name}}"]
