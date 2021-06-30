import pytest


def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="default username")
    parser.addoption("--password", action="store", default="default password")


@pytest.fixture
def username(request):
    return request.config.getoption("--username")


@pytest.fixture
def password(request):
    return request.config.getoption("--password")
