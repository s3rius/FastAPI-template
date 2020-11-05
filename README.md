<div align="center">
<img src="images/logo.png" width=700>
<div><i>Fast and flexible general-purpose template for your API.</i></div>
</div>

## Usage
⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/), and [Docker-compose](https://docs.docker.com/compose/install/) must be installed and accessible ⚠️

```bash
python3 -m pip install cookiecutter
cookiecutter gh:s3rius/FastAPI-template
# Answer prompts questions
# ???
# 🍪 Enjoy your new project 🍪
cd new_project
docker-compose up --build
```

## Features
Currently supported features:
- redis
- systemd units
- Example (dummy) SQLAlchemy model
- Elastic Search support
- Scheduler support

Planned features:
- Add Makefile support
