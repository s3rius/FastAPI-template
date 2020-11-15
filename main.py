from pathlib import Path

from cookiecutter.exceptions import FailedHookException, OutputDirExistsException
from cookiecutter.main import cookiecutter
from termcolor import cprint

script_dir = Path(__file__).parent


def main():
    try:
        cookiecutter(template=f"{script_dir}/template")
    except (FailedHookException, OutputDirExistsException) as exc:
        if isinstance(exc, OutputDirExistsException):
            cprint(
                "Directory with such name already exists!",
                "red"
            )
        return
    cprint("Project successfully generated. You can read information about usage in README.md")


if __name__ == "__main__":
    main()
