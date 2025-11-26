import os
from pathlib import Path
import shlex
import subprocess
from typing import Any

import yaml
from fastapi_template.input_model import BuilderContext
from fastapi_template.__main__ import generate_project


def generate_project_and_chdir(context: BuilderContext):
    generate_project(context)
    os.chdir(context.project_name)


def run_pre_commit() -> int:
    return os.system("pre-commit run -a")


def run_docker_compose_command(
    command: str,
) -> int:
    docker_command = ["docker", "compose"]
    docker_command.extend(shlex.split(command))
    return os.system(shlex.join(docker_command))


def run_default_check(context: BuilderContext, worker_id: str, without_pytest=False):
    generate_project_and_chdir(context)
    compose = Path("./docker-compose.yml")
    with compose.open("r") as compose_file:
        data = yaml.safe_load(compose_file)
    data["services"]["api"]["image"] = f"test_image:v{worker_id}"
    with compose.open("w") as compose_file:
        yaml.safe_dump(data, compose_file)

    assert run_pre_commit() == 0

    if without_pytest:
        return

    build = run_docker_compose_command("--progress=plain build")
    assert build == 0
    tests = run_docker_compose_command("--progress=plain run --rm api pytest -vv .")
    assert tests == 0


def model_dump_compat(model: Any):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
