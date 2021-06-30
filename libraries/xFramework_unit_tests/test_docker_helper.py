import pytest
from libraries.helper.docker_helper import DockerHelper

default_artifactory_url = "docker.artifactory01.ghdna.io/csrm_emerald:1.0-RC1"
default_volumes = {'Opt': {'bind': '/opt/tests/csrm/data/', 'mode': 'rw'}}


def test_gid_204899_get_new_container():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    container = docker_helper.get_new_container(artifactory_url=default_artifactory_url, volumes=default_volumes)
    exit_code, output = container.exec_run("ls")
    assert exit_code == 0
    assert "VERSION.txt" in output.decode('ascii')


def test_gid_204900_get_new_container_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    with pytest.raises(Exception):
        docker_helper.get_new_container(artifactory_url="nonexistent container", volumes=default_volumes)


def test_gid_204901_get_existing_container():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    original_container = docker_helper.get_new_container(artifactory_url=default_artifactory_url,
                                                         volumes=default_volumes)
    existing_container = docker_helper.get_existing_container(original_container.id)
    assert original_container == existing_container


def test_gid_204902_get_existing_container_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    with pytest.raises(Exception):
        docker_helper.get_existing_container("nonexistent container")


def test_gid_204903_run():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    container = docker_helper.get_new_container(artifactory_url=default_artifactory_url, volumes=default_volumes)
    version_cmd = "cat /app/VERSION.txt"
    version_from_run = docker_helper.run(container, version_cmd).decode('ascii').strip()
    exit_code, output = container.exec_run(version_cmd)
    assert exit_code == 0
    assert version_from_run == output.decode('ascii').strip()


# For this test case we can just check that we get a non-zero exit code
def test_gid_204904_run_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    docker_helper = DockerHelper()
    container = docker_helper.get_new_container(artifactory_url=default_artifactory_url, volumes=default_volumes)
    exit_code, output = docker_helper.run(container, "nonexistent command")
    assert exit_code != 0
