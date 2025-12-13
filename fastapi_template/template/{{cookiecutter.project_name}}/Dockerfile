# -----------------------------------
# STAGE BUILDER: Prepare builder image
# Only install main dependencies
# -----------------------------------
FROM ghcr.io/astral-sh/uv:0.9.17-python3.13-bookworm-slim AS builder

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

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/.venv \
    VIRTUAL_ENV="/opt/.venv" \
    PATH="/opt/.venv/bin:$PATH" \
    {%- if cookiecutter.orm == 'piccolo' %}
    PICCOLO_CONF="{{cookiecutter.project_name}}.piccolo_conf" \
    {%- endif %}
    UV_NO_DEV=1

WORKDIR /app/src

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# -----------------------------------
# STAGE PROD: Production image
# Copy dependencies and environment from builder image
# -----------------------------------
FROM python:3.13-slim-bookworm AS prod

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

ENV VIRTUAL_ENV="/opt/.venv" \
    {%- if cookiecutter.orm == 'piccolo' %}
    PICCOLO_CONF="{{cookiecutter.project_name}}.piccolo_conf" \
    {%- endif %}
    PATH="/opt/.venv/bin:$PATH" \

COPY --from=builder --chown=nonroot:nonroot /app/src /app/src
COPY --from=builder --chown=nonroot:nonroot /opt/.venv /opt/.venv

USER nonroot

WORKDIR /app/src

# -----------------------------------
# STAGE DEVELOPMENT: Development image
# Copy dependencies and environment from builder image and add dev dependencies
# -----------------------------------
FROM builder AS dev

ENV UV_NO_DEV=0

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --all-groups
