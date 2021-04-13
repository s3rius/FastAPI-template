#!/usr/bin/env python
import json
import os
import shutil
from argparse import Namespace

import pre_commit.constants as pre_commit_constants
import pre_commit.main as pre_commit
from pygit2 import init_repository
from termcolor import cprint

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
        for feature in manifest['features']:
            if not feature['enabled'] == "true":
                print("removing resources for disabled feature {}...".format(feature['name']))
                for resource in feature['resources']:
                    delete_resource(resource)
    print("cleanup complete, removing manifest...")
    delete_resource(MANIFEST)


def init_repo():
    store = pre_commit.Store()
    repo_path = os.getcwd()
    repo = init_repository(repo_path)
    cprint("Git repository initialized.", "green")
    repo.index.add_all()
    repo.index.write()
    cprint("Added files to index.", "green")
    pre_commit.install(
        config_file=pre_commit_constants.CONFIG_FILE,
        store=store,
        hook_types=["pre-commit"],
        overwrite=False
    )
    cprint("pre-commit installed.", "green")
    run_namespace = Namespace(
        all_files=True,
        files=[],
        hook_stage='commit',
        from_ref=None,
        to_ref=None,
        remote_name=None,
        checkout_type=None,
        hook=None,
        verbose=False,
        color=True,
        show_diff_on_failure=False,
        is_squash_merge=False,
    )
    pre_commit.run(
        config_file=pre_commit_constants.CONFIG_FILE,
        store=store,
        args=run_namespace
    )
    repo.index.add_all()
    repo.index.write()


if __name__ == "__main__":
    delete_resources_for_disabled_features()
    init_repo()
