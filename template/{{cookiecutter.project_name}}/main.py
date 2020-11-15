import argparse
from typing import Any, Dict, Optional

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication

from src.server import app


class StandaloneApplication(BaseApplication):
    def __init__(self, application_instance: FastAPI, run_options: Optional[Dict[str, Any]] = None):
        self.options = run_options or {}
        self.application = application_instance
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> FastAPI:
        return self.application


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--pid-file", type=str, default="/tmp/{{cookiecutter.project_name}}.pid")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    options = {
        "bind": f"{args.host}:{args.port}",
        "workers": 4,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "pidfile": args.pid_file,
    }
    StandaloneApplication(app, options).run()
