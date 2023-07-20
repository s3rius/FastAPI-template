import os
import shutil

import uvicorn

{%- if cookiecutter.gunicorn == "True" %}
from {{cookiecutter.project_name}}.gunicorn_runner import GunicornApplication
{%- endif %}
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
    {%- if cookiecutter.gunicorn == "True" %}
    if settings.reload:
        uvicorn.run(
            "{{cookiecutter.project_name}}.web.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doen't work with Uvicorn workers.
        GunicornApplication(
            "{{cookiecutter.project_name}}.web.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',  # noqa: WPS323
        ).run()
    {%- else %}
    uvicorn.run(
        "{{cookiecutter.project_name}}.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )
    {%- endif %}

if __name__ == "__main__":
    main()
