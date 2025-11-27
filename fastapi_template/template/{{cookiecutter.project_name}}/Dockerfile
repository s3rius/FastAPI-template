FROM ghcr.io/astral-sh/uv:0.9.12-bookworm AS uv

# -----------------------------------
# STAGE 1: prod stage
# Only install main dependencies
# -----------------------------------
FROM python:3.13-slim-bookworm AS prod

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

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_MANAGED_PYTHON=1
{%- if cookiecutter.orm == 'piccolo' %}
ENV PICCOLO_CONF="{{cookiecutter.project_name}}.piccolo_conf"
{%- endif %}

WORKDIR /app/src

RUN --mount=from=uv,source=/usr/local/bin/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .

RUN --mount=from=uv,source=/usr/local/bin/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

CMD ["/usr/local/bin/python", "-m", "{{cookiecutter.project_name}}"]

# -----------------------------------
# STAGE 3: development build
# Includes dev dependencies
# -----------------------------------
FROM prod AS dev

RUN --mount=from=uv,source=/usr/local/bin/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --all-groups
