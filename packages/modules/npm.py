from urllib import request
import requests
import semver

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"


def get_package_with_transitive_dependencies(name: str, range: str) -> VersionedPackage:
    """
    Recursively request package dependencies with all transitive dependencies.
    Args:
        name (str): name of the package
        range (str): range of the dependencies

    Returns:
        VersionedPackage: _description_
    """
    package, dependencies = request_package(name, range)
    package.dependencies = [
        get_package_with_transitive_dependencies(name=dep_name, range=dep_range) for dep_name, dep_range in dependencies.items()
    ]

    return package


def request_package(name: str, range: str) -> tuple[VersionedPackage, dict]:
    url = f"{NPM_REGISTRY_URL}/{name}"

    npm_package = requests.get(url).json()

    versions = list(npm_package["versions"].keys())
    version = semver.max_satisfying(versions, range)
    version_record = npm_package["versions"][version]

    return VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    ), version_record.get("dependencies", {})
