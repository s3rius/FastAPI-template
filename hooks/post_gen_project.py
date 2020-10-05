#!/usr/bin/env python
import os
import shutil
import subprocess
import sys

import yaml

MANIFEST = "conditional_files.yaml"
FIRST_RUN_WIN = "first_run.bat"
FIRST_RUN = "first_run.sh"


def delete_resource(resource):
    if os.path.isfile(resource):
        print("removing file: {}".format(resource))
        os.remove(resource)
    elif os.path.isdir(resource):
        print("removing directory: {}".format(resource))
        shutil.rmtree(resource)


def delete_resources_for_disabled_features():
    with open(MANIFEST) as manifest_file:
        manifest = yaml.safe_load(manifest_file)
        for feature in manifest['features']:
            if not feature['enabled']:
                print("removing resources for disabled feature {}...".format(feature['name']))
                for resource in feature['resources']:
                    delete_resource(resource)
    print("cleanup complete, removing manifest...")
    delete_resource(MANIFEST)


def init_repo():
    if sys.platform == 'win32':
        subprocess.run([FIRST_RUN_WIN])
        return
    else:
        subprocess.run(['sh', FIRST_RUN])
    delete_resource(FIRST_RUN)
    delete_resource(FIRST_RUN_WIN)
    subprocess.run(['git', 'add', '.'])


if __name__ == "__main__":
    delete_resources_for_disabled_features()
    init_repo()
