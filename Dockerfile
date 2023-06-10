FROM python:3.9.17-alpine

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
  mariadb-connector-c-dev \
  # For UI \
  ncurses \
  bash

RUN adduser --disabled-password fastapi_template
RUN mkdir /projects /src
RUN chown -R fastapi_template:fastapi_template /projects /src
USER fastapi_template

WORKDIR /src

ENV PATH ${PATH}:/home/fastapi_template/.local/bin

RUN pip install poetry==1.4.2

COPY . /src/
RUN pip install .

USER root
RUN rm -rfv /src
RUN apk del curl
USER fastapi_template

RUN git config --global user.name "Fastapi Template"
RUN git config --global user.email "fastapi-template@no-reply.com"

VOLUME /projects
WORKDIR /projects

ENTRYPOINT ["/home/fastapi_template/.local/bin/fastapi_template"]

