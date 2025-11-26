FROM ghcr.io/astral-sh/uv:0.9.12-python3.13-alpine

RUN apk update && apk add --no-cache \
  curl \
  # For building dependencies. \
  gcc \
  musl-dev \
  git \
  g++ \
  libffi-dev \
  # For psycopg \
  postgresql-dev \
  # For mysql deps \
  mariadb-dev \
  # For UI \
  ncurses \
  bash

RUN adduser -u 1000 --disabled-password fastapi_template
RUN mkdir /projects /src

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_MANAGED_PYTHON=1

WORKDIR /src
COPY . .

ENV PATH="${PATH}:/usr/local/bin"

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

RUN apk del curl

RUN chown -R fastapi_template:fastapi_template /projects /src /usr/local/lib/

USER fastapi_template

RUN git config --global user.name "Fastapi Template"
RUN git config --global user.email "fastapi-template@no-reply.com"

VOLUME /projects
WORKDIR /projects

ENTRYPOINT ["python", "-m", "fastapi_template"]
