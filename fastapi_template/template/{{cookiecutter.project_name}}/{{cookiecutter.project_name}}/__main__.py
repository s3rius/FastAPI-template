import uvicorn
import os
import shutil

from {{cookiecutter.project_name}}.settings import settings


{%- if cookiecutter.prometheus_enabled == "True" %}
def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    os.makedirs(settings.prometheus_dir, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
{%- endif %}


def main() -> None:
    """Entrypoint of the application."""
    {%- if cookiecutter.prometheus_enabled == "True" %}
    set_multiproc_dir()
    {%- endif %}
    {%- if cookiecutter.orm == "piccolo" %}
    os.environ['PICCOLO_CONF'] = "{{cookiecutter.project_name}}.piccolo_conf"
    {%- endif %}
    uvicorn.run(
        "{{cookiecutter.project_name}}.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
