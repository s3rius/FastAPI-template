#!/usr/bin/env python
import json
import os
import shutil
import subprocess

from termcolor import cprint, colored
from pathlib import Path

CONDITIONAL_MANIFEST = "conditional_files.json"
REPLACE_MANIFEST = "replaceable_files.json"


def delete_resource(resource):
    if os.path.isfile(resource):
        os.remove(resource)
    elif os.path.isdir(resource):
        shutil.rmtree(resource)


def delete_resources_for_disabled_features():
    with open(CONDITIONAL_MANIFEST) as manifest_file:
        manifest = json.load(manifest_file)
        for feature_name, feature in manifest.items():
            if feature["enabled"].lower() != "true":
                text = "{} resources for disabled feature {}...".format(
                    colored("Removing", color="red"),
                    colored(feature_name, color="magenta", attrs=["underline"]),
                )
                print(text)
                for resource in feature["resources"]:
                    delete_resource(resource)
    delete_resource(CONDITIONAL_MANIFEST)
    cprint("cleanup complete!", color="green")


def replace_resources():
    print(
        "⭐ Placing {} nicely in your {} ⭐".format(
            colored("resources", color="green"), colored("new project", color="blue")
        )
    )
    with open(REPLACE_MANIFEST) as replace_manifest:
        manifest = json.load(replace_manifest)
        for target, replaces in manifest.items():
            target_path = Path(target)
            delete_resource(target_path)
            for src_file in map(Path, replaces):
                if src_file.exists():
                    shutil.move(src_file, target_path)
    delete_resource(REPLACE_MANIFEST)
    print(
        "Resources are happy to be where {}.".format(
            colored("they are needed the most", color="green", attrs=["underline"])
        )
    )


def init_repo():
    subprocess.run(["git", "init"], stdout=subprocess.PIPE)
    cprint("Git repository initialized.", "green")
    subprocess.run(["git", "add", "."], stdout=subprocess.PIPE)
    cprint("Added files to index.", "green")
    subprocess.run(["poetry", "install", "-n"])
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    cprint("pre-commit installed.", "green")
    subprocess.run(["poetry", "run", "pre-commit", "run", "-a"])
    subprocess.run(["git", "add", "."], stdout=subprocess.PIPE)
    subprocess.run(["git", "commit", "-m", "Initial commit"], stdout=subprocess.PIPE)

if __name__ == "__main__":
    delete_resources_for_disabled_features()
    replace_resources()
    init_repo()
