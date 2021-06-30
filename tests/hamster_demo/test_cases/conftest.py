import pytest
import logging
from pathlib import Path
import libraries.helper as helper
import libraries.framework as framework
from .config import Config
from tests.hamster_demo.libraries.titanite_bip352 import Titanite_v1
from tests.hamster_demo.libraries.titanite_bip353 import Titanite_v2
logger = logging.getLogger(__name__) 


@pytest.fixture(scope="session")
def app_config(test_version): #Refer to top level conftest for test_version fixture
    cfg = Config(test_version)
    return cfg

@pytest.fixture(scope="session")
def Titanite(app_config):
    return app_config.csrm_version

def verify_build_version(app_config, container):
    expected_build_version = app_config.build_version
    cmd = "cat /app/VERSION.txt"
    actual_version = helper.docker_helper.run(container, cmd)
    actual_version = actual_version.decode()
    assert expected_build_version in actual_version, "actual build {} did not match build version {}".format(actual_version, expected_build_version)

@pytest.fixture(scope="session")
def titanite_container(app_config):
    artifactory_url = app_config.artifactory_url
    container = helper.docker_helper.get_new_container(artifactory_url=artifactory_url, volumes=app_config.docker_volumes)
    verify_build_version(app_config, container)
    logger.info('returning container from {} with name {}'.format(artifactory_url, container.name))
    yield container
    logger.info("container exiting {}".format(container.name))
    container.stop()
    container.remove(force=True)

@pytest.fixture(scope="function")
def general_dataset(request, save_run_data): #Refer to top level conftest for save_run_data
    data_path = Path(__file__).parent.parent / "data"
    bash_command = "git checkout {} ".format(data_path)
    helper.subprocess_helper.run(bash_command)
    bash_command = "git clean -xf {} ".format(data_path)
    helper.subprocess_helper.run(bash_command)
    """
    yield
    test_case_name_parser = framework.Test_case_name_parser(request)
    destination = Path(__file__).parent.parent / "logs/TestCaseData" / test_case_name_parser.get_test_case_name()
    bash_command = "cp -r {} {}".format(data_path, destination)
    helper.subprocess_helper.run(bash_command)
    """
    





