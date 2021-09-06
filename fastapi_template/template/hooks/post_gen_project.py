#!/usr/bin/env python
import json
import os
import shutil
import subprocess

from pygit2 import init_repository
from termcolor import cprint, colored

MANIFEST = "conditional_files.json"


def delete_resource(resource):
    if os.path.isfile(resource):
        print("removing file: {}".format(resource))
        os.remove(resource)
    elif os.path.isdir(resource):
        print("removing directory: {}".format(resource))
        shutil.rmtree(resource)


def delete_resources_for_disabled_features():
    with open(MANIFEST) as manifest_file:
        manifest = json.load(manifest_file)
        for feature_name, feature in manifest.items():
            if feature['enabled'].lower() != "true":
                text = "{} resources for disabled feature {}...".format(
                    colored("Removing", color="red"),
                    colored(feature_name, color="magenta", attrs=['underline'])
                )
                print(text)
                for resource in feature['resources']:
                    delete_resource(resource)
    delete_resource(MANIFEST)
    cprint("cleanup complete!", color="green")


def init_repo():
    repo_path = os.getcwd()
    repo = init_repository(repo_path)
    cprint("Git repository initialized.", "green")
    repo.index.add_all()
    repo.index.write()
    cprint("Added files to index.", "green")
    subprocess.run(["poetry", "install", "-n"])
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    cprint("pre-commit installed.", "green")
    subprocess.run(["poetry", "run", "pre-commit", "run", "-a"])
    repo.index.add_all()
    repo.index.write()


if __name__ == "__main__":
    delete_resources_for_disabled_features()
    init_repo()
