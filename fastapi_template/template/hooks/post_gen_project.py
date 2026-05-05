#!/usr/bin/env python
import shutil
import subprocess
import tomllib
import shlex

from termcolor import cprint, colored
from pathlib import Path

CONDITIONAL_MANIFEST = Path("conditional_files.toml")
REPLACE_MANIFEST = Path("replaceable_files.toml")


def delete_resource(resource: Path):
    if resource.is_file():
        resource.unlink()
    elif resource.is_dir():
        shutil.rmtree(resource)


def delete_resources_for_disabled_features():
    with CONDITIONAL_MANIFEST.open("rb") as manifest_file:
        manifest = tomllib.load(manifest_file)

        for feature in manifest["features"]:
            enabled = feature["enabled"].lower() != "true"
            name = feature["name"]
            resources = feature["resources"]
            if enabled:
                text = "{} resources for disabled feature {}...".format(
                    colored("Removing", color="red"),
                    colored(name, color="magenta", attrs=["underline"]),
                )
                print(text)
                for resource in resources:
                    delete_resource(Path(resource))
    delete_resource(CONDITIONAL_MANIFEST)
    cprint("cleanup complete!", color="green")


def replace_resources():
    print(
        "⭐ Placing {} nicely in your {} ⭐".format(
            colored("resources", color="green"), colored("new project", color="blue")
        )
    )
    with REPLACE_MANIFEST.open("rb") as replace_manifest:
        manifest = tomllib.load(replace_manifest)
        for substitution in manifest["sub"]:
            target = Path(substitution["target"])
            replaces = [Path(path) for path in substitution["replaces"]]
            delete_resource(target)
            for src_file in replaces:
                if src_file.exists():
                    shutil.move(src_file, target)
    delete_resource(REPLACE_MANIFEST)
    print(
        "Resources are happy to be where {}.".format(
            colored("they are needed the most", color="green", attrs=["underline"])
        )
    )


def run_cmd(cmd: str, ignore_error: bool = False):
    out = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if out.returncode != 0 and not ignore_error:
        cprint(" WARNING ".center(50, "="))
        cprint(
            f"[WARN] Command `{cmd}` was not successfull. Check output below.",
            "yellow",
        )
        cprint(
            "However, the project was generated. So it could be a false-positive.",
            "yellow",
        )
        if out.stdout:
            cprint(out.stdout.decode(errors="replace"), "red")
        if out.stderr:
            cprint(out.stderr.decode(errors="replace"), "red")
        raise ValueError()


def init_repo():
    run_cmd("git init")
    cprint(" Git repository initialized", "green")
    run_cmd("git add .")
    cprint("🐍 Installing python dpendencies with UV", "green")
    run_cmd("uv sync")
    run_cmd("uv run pre-commit install")
    cprint("📚🖌️📄📏 Tidying up the project", "green")
    for _ in range(2):
        run_cmd("uv run pre-commit run -a", ignore_error=True)
    run_cmd("git add .")
    cprint("🚀Creating your first commit", "green")
    run_cmd("git commit -m 'Initial commit'")


if __name__ == "__main__":
    delete_resources_for_disabled_features()
    replace_resources()
    try:
        init_repo()
    except ValueError:
        pass
