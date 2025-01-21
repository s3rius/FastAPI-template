import os
from pathlib import Path
import shlex
import subprocess
from typing import Any, Optional

import yaml
from fastapi_template.input_model import BuilderContext
from fastapi_template.__main__ import generate_project


def generate_project_and_chdir(context: BuilderContext):
    generate_project(context)
    os.chdir(context.project_name)


def run_pre_commit() -> int:
    results = subprocess.run(["pre-commit", "run", "-a"])
    return results.returncode


def run_docker_compose_command(
    command: Optional[str] = None,
) -> subprocess.CompletedProcess:
    docker_command = ["docker", "compose"]
    if command:
        docker_command.extend(shlex.split(command))
    else:
        docker_command.extend(["build"])
    return subprocess.run(docker_command)


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

    build = run_docker_compose_command("build")
    assert build.returncode == 0
    tests = run_docker_compose_command("run --rm api pytest -vv .")
    assert tests.returncode == 0


def model_dump_compat(model: Any):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
