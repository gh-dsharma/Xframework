import pytest
import logging
import libraries.helper as helper
import libraries.framework as framework

def pytest_addoption(parser):
    parser.addoption(
        "--test-version", 
        action="store",
        help="Version of software to run",
        default="v1"
    )
    parser.addoption(
        "--save-run-data", 
        action="store",
        help="Save run data",
        default=False
    )

    parser.addoption(
        "--logging-level", 
        action="store",
        help="Sets the level for logging. https://docs.python.org/3/library/logging.html#levels",
        default='INFO'
    )

@pytest.fixture(scope='session') 
def test_version(request):
    return request.config.getoption("--test-version") 

@pytest.fixture(scope='session') 
def save_run_data(request):
    return request.config.getoption("--save-run-data") 

@pytest.fixture(scope='session') 
def logging_level(request):
    return request.config.getoption("--logging-level") 

@pytest.fixture(scope="function")
def testcase_logger(request, logging_level):
    yield from framework.testcase_logger(request, logging_level)

