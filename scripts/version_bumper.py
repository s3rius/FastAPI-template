import argparse
from pathlib import Path
import re
import requests
from packaging.version import Version

DEP_RE = re.compile(r"\s*\"(?P<package>.+)\s*(?P<constraints>\>\=.+,\<.+)\s*\"")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        type=Path,
    )
    return parser.parse_args()


def get_new_version(package_name: str) -> Version:
    name = package_name.split("[")[0]
    print("Fetching new version for", name)
    resp = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    resp.raise_for_status()
    rjson = resp.json()
    return Version(rjson["info"]["version"])


def main():
    args = parse_args()
    file: Path = args.file
    lines = []
    known_versions = {}
    with file.open("r") as f:
        for line in f:
            match = DEP_RE.match(line)
            if not match:
                lines.append(line)
                continue
            full_package = match.group("package").strip()
            package = full_package.strip().split("[")[0]
            if package in known_versions:
                print("Using known version for", package)
                version = known_versions[package]
            else:
                version = get_new_version(package)
                known_versions[package] = version
            upper_version = version.major + 1
            constraints = match.group("constraints").strip().split(";")
            markers = None
            if len(constraints) == 2:
                markers = constraints[1]
            new_constraints = f">={version},<{upper_version}"
            if markers:
                new_constraints += f"; {markers}"
            lines.append('  "' + full_package + " " + new_constraints + '",\n')
    with file.open("w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    main()
