import os
import re
import shutil
import tempfile
from pathlib import Path

import pytest
from faker import Faker
from fastapi_template.input_model import BuilderContext, Database
from fastapi_template.tests.utils import run_docker_compose_command, model_dump_compat

@pytest.fixture
def project_name(worker_id: str) -> str:
    """
    Generate name for test project.

    :return: project name.
    """
    fake = Faker()
    raw_name = fake.name_female() + worker_id
    clear_name: str = (
        raw_name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")
    )
    return re.sub("_+", "_", clear_name).strip("_")


@pytest.fixture(scope="session", autouse=True)
def generator_start_dir() -> str:
    """
    Generate directory to work into

    :yield: this fixture generates dir for all test projects.
    """
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    try:
        yield newpath
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(newpath, ignore_errors=True)


@pytest.fixture()
def default_context(project_name: str) -> None:
    """
    Default builder context without features.

    :param project_name: current project name.
    :return: context.
    """
    return BuilderContext(
        project_name=project_name,
        kube_name=project_name.replace("_", "-"),
        api_type="rest",
        ci_type="none",
        db="none",
        db_info=model_dump_compat(Database(name="none")),
        enable_redis=False,
        enable_taskiq=False,
        enable_migrations=False,
        enable_kube=False,
        enable_routers=True,
        add_dummy=False,
        self_hosted_swagger=False,
        enable_rmq=False,
        prometheus_enabled=False,
        otlp_enabled=False,
        sentry_enabled=False,
        force=True,
    )


@pytest.fixture(autouse=True)
def default_dir(generator_start_dir: str) -> None:
    """
    Change directory to generator_start_dir.

    :param generator_start_dir: start_dir.
    """
    yield
    cwd = os.getcwd()
    if cwd != generator_start_dir:
        os.chdir(generator_start_dir)


@pytest.fixture(autouse=True)
def docker_module_shutdown(generator_start_dir: str, project_name: str) -> None:
    """
    Cleans up docker context.

    :param generator_start_dir: generator dir.
    :param project_name: name of the project.
    """
    yield
    cwd = os.getcwd()
    project_dir = Path(generator_start_dir) / project_name
    if not project_dir.exists():
        return
    os.chdir(project_dir)
    Path("poetry.lock").unlink(missing_ok=True)
    run_docker_compose_command("down -v")
    os.chdir(cwd)
