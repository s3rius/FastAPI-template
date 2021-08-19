FROM python:3.9.6-slim-buster

RUN useradd -m {{cookiecutter.project_name}}

USER {{cookiecutter.project_name}}

ENV PATH="${PATH}:/home/{{cookiecutter.project_name}}/.poetry/bin:/home/{{cookiecutter.project_name}}/.local/bin"

RUN pip install poetry==1.1.7

# Installing requirements
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /home/{{cookiecutter.project_name}}/app/
WORKDIR /home/{{cookiecutter.project_name}}/app/

RUN poetry install --no-dev

# Copying actuall application
COPY . /home/{{cookiecutter.project_name}}/app/src/
WORKDIR /home/{{cookiecutter.project_name}}/app/src/
RUN pip install --use-feature=in-tree-build  .

WORKDIR /home/{{cookiecutter.project_name}}/app

USER root
RUN rm -rf /home/{{cookiecutter.project_name}}/app/src
RUN chown -R {{cookiecutter.project_name}} /home/{{cookiecutter.project_name}}
RUN chmod -R 700 /home/{{cookiecutter.project_name}}
USER {{cookiecutter.project_name}}

CMD python -m {{cookiecutter.project_name}}
