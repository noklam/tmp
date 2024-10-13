from django.test import Client
import pytest


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def latest_version_minimatch():
    response = {
        "name": "minimatch",
        "version": "10.0.1",
        "dependencies": [
            {
                "name": "brace-expansion",
                "version": "2.0.1",
                "dependencies": [
                    {"name": "balanced-match", "version": "1.0.2", "dependencies": []}
                ],
            }
        ],
    }
    return response


def test_get_package_redirect_without_trailing_slash(client, latest_version_minimatch):
    response = client.get("/package/minimatch", follow=True)  # redirect
    assert response.status_code == 200
    assert response.json() == latest_version_minimatch


def test_get_package_without_version(client, latest_version_minimatch):
    response = client.get("/package/minimatch/")
    assert response.status_code == 200
    assert response.json() == latest_version_minimatch


def test_get_package(client):
    response = client.get("/package/minimatch/3.1.2")
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [
            {
                "dependencies": [
                    {"dependencies": [], "name": "balanced-match", "version": "1.0.2"},
                    {"dependencies": [], "name": "concat-map", "version": "0.0.1"},
                ],
                "name": "brace-expansion",
                "version": "1.1.11",
            }
        ],
        "name": "minimatch",
        "version": "3.1.2",
    }


def test_get_package_with_range(client, latest_version_minimatch):
    response = client.get("/package/minimatch/>=3.1.2")
    assert response.status_code == 200
    assert response.json() == latest_version_minimatch


def test_get_package_with_invalid_range(client, latest_version_minimatch):
    range = ">=999.99.9"
    package_name = "minimatch"
    response = client.get(f"/package/{package_name}/{range}")
    assert response.status_code == 200
    assert response.json() == f"{package_name} version not found: {range}"
