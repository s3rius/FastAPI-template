import os
import subprocess
from typing import Optional
from fastapi_template.input_model import BuilderContext
from fastapi_template.__main__ import generate_project


def generate_project_and_chdir(context: BuilderContext):
    generate_project(context)
    os.chdir(context.project_name)


def run_pre_commit() -> int:
    results = subprocess.run(["pre-commit", "run", "-a"])
    return results.returncode


def run_docker_compose_command(command: Optional[str] = None) -> subprocess.CompletedProcess:
    docker_command = [
        "docker-compose",
        "-f",
        "deploy/docker-compose.yml",
        "--project-directory",
        ".",
    ]
    if command:
        docker_command.extend(command.split())
    else:
        docker_command.extend(
            [
                "build",
            ]
        )
    return subprocess.run(docker_command)


def run_default_check(context: BuilderContext):
    generate_project_and_chdir(context)
    assert run_pre_commit() == 0
    build = run_docker_compose_command("build")
    assert build.returncode == 0
    tests = run_docker_compose_command("run --rm api pytest -vv .")
    assert tests.returncode == 0
