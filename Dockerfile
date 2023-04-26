FROM python:3.9.7-alpine3.13 AS builder

RUN apk add --no-cache \
  # For building dependencies. \
  gcc \
  musl-dev \
  g++ \
  libffi-dev \
  # For psycopg \
  postgresql-dev \
  # For mysql deps \
  mariadb-connector-c-dev

COPY pyproject.toml poetry.lock README.md /src/
COPY ./fastapi_template /src/fastapi_template/
WORKDIR /src

RUN python -m venv --copies /src/venv
RUN /src/venv/bin/pip install poetry==1.4.2
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    . /src/venv/bin/activate && poetry install --only main

FROM python:3.9.7-alpine3.13

RUN apk add --no-cache git ncurses
RUN adduser --disabled-password fastapi_template
RUN mkdir /projects /src
RUN chown -R fastapi_template:fastapi_template /projects /src
USER fastapi_template

COPY --from=builder /src/venv /src/venv/
COPY ./fastapi_template /src/fastapi_template/
WORKDIR /src

ENV PATH ${PATH}:/src/venv/bin

USER fastapi_template

VOLUME /projects
WORKDIR /projects

ENTRYPOINT ["/src/venv/bin/fastapi_template"]

