FROM python:3.9.7-alpine3.13

RUN apk add --no-cache \
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
  mariadb-connector-c-dev

RUN adduser --disabled-password fastapi_template
RUN mkdir /projects /src
RUN chown -R fastapi_template:fastapi_template /projects /src
USER fastapi_template

WORKDIR /src

ENV PATH ${PATH}:/home/fastapi_template/.local/bin

RUN pip install poetry==1.1.11

COPY . /src/
RUN pip install .

USER root
RUN rm -rfv /src
RUN apk del curl
USER fastapi_template

VOLUME /projects
WORKDIR /projects

ENTRYPOINT ["/home/fastapi_template/.local/bin/fastapi_template"]

