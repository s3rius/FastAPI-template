FROM python:3.9.6-slim-buster

RUN apt-get update && apt-get install -y \
    wait-for-it \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ENV PATH="${PATH}:/home/{{cookiecutter.project_name}}/.poetry/bin:/home/{{cookiecutter.project_name}}/.local/bin"

RUN pip install poetry==1.1.8

# Installing requirements
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

RUN poetry install --no-dev

# Copying actuall application
COPY . /app/src/
RUN pip install --use-feature=in-tree-build  .

{%- if cookiecutter.db_info.name == "sqlite" %}
VOLUME [ "/db_data" ]
{%- endif %}

CMD python -m {{cookiecutter.project_name}}
