# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## For developers

To run project locally you can just type `docker-compose up`

### Needed environment variables for CI\CD
* APP_ENV_FILE - path to .env file on server

## How to run the application

At first, you need to install all dependencies with poetry

```bash
poetry install
```

For tests you need to set all needed environment variables.
All needed variables shown in `envs/.env.example`.

If all new environment parameters are stored in .env file, then you better to start testing/application using `dotenv` program, or set  `EnvironmentFile` in your systemd-module. 

### Applying migrations and startup
Before running the application don't forget to apply pending migrations. To do so run the following command in the application directory:
```bash
dotenv -f ".env.file" run alembic upgrade head;
```

To test and start the application with `dotenv` run following commands: 
```bash
# Testing
dotenv -f envs/test.env run pytest
# Startup
dotenv -f envs/.env run uvicorn --access-log --log-level debug --host 0.0.0.0 --port 8100 src.server:app
```

If all environment variables already set: 
```bash
# Testing
pytest
# Startup
uvicorn --access-log --log-level debug --host 0.0.0.0 --port 8100 src.server:app
```

Example of configured systemd module for application shown in [systemd/{{cookiecutter.project_name}}_service.service](systemd/{{ cookiecutter.project_name }}_service.service) file.


## Task scheduler startup
Task scheduler is a script that runs background tasks periodically.
You can read more about scheduler at [aioschedule docs](https://pypi.org/project/aioschedule/) 

```bash
# Command to run scheduler script with existing environment variables:
python scheduler.py
 
# Command to run sceduler with .env file: 
dotenv -f envs/.env run python scheduler.py
```

Example of configured systemd module for scheduler shown in [systemd/{{cookiecutter.project_name}}_scheduler.service](systemd/{{ cookiecutter.project_name }}_scheduler.service)

## About systemd files

To use systemd files on different machine you may need to change following parameters:
* EnvironmentFile - absolute path to .env file to use during execution;
* WorkingDirectory - absolute path to project directory on your machine or server;
* ExecStart - command to start the application.