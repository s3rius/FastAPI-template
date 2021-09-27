FROM python:3.9.6-slim-buster

RUN apt-get update && apt-get install -y \
    wait-for-it \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.1.8

# Installing requirements
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

RUN poetry install

# Copying actuall application
COPY . /app/src/
RUN pip install --use-feature=in-tree-build  .

CMD python -m {{cookiecutter.project_name}}
