import logging
import docker
from .logging_helper import library_logger

logger = logging.getLogger(__name__) #framework.libraries.helper

class DockerConfig:
    auth_config = {
                'username': 'ghbi_service',
                'password': 'Password123',
    }
    volume_to_mount = {'/ghds/': {'bind': '/ghds/', 'mode': 'rw'}}

class DockerHelper():
    client = docker.from_env()

    @staticmethod
    def get_new_container(artifactory_url, *args, **kwargs) -> 'docker container':
        """
        Get a container instance from a URL.
        https://docker-py.readthedocs.io/en/stable/containers.html

        :Usage:
            artifactory_url = "docker.artifactory01.ghdna.io/csrm_emerald:1.0-RC1"
            container = helper.subprocess_helper.create_container(artifactory_url)
        :Returns:
            a container
        """
        DockerHelper.client.images.pull(artifactory_url, auth_config=DockerConfig.auth_config)
        if 'volumes' in kwargs:
            kwargs['volumes'].update(DockerConfig.volume_to_mount)
        else:
            kwargs['volumes'] = DockerConfig.volume_to_mount
        container = DockerHelper.client.containers.run(artifactory_url, command="/bin/bash", tty=True, detach=True, *args, **kwargs)
        logger.info('returning container from {}'.format(artifactory_url))
        return container

    @staticmethod
    def get_existing_container(id_or_name):
        return DockerHelper.client.containers.get(id_or_name)

    @staticmethod
    def run(container: 'docker container', container_command: str, *args, **kwargs):
        """
        Invoke the container 
        :Usage:
            container_command = "/opt/conda/bin/python3 /app/emerald.py --input_dir {}".format(test_case_directory)
            helper.docker_helper.run(container, container_command)
        :Returns:
            stdout or tuple containg exit code and (stdout, stderr)
        """
        exit_code, output = container.exec_run(container_command, demux=True, *args, **kwargs) #demux explanation: https://docker-py.readthedocs.io/en/stable/containers.html
        logger.info("container: {} image: {}\n executing: {}".format(container.name, container.image, container_command))
        if exit_code == 0:
            return output[0] #just return stdout, stderr will be empty since exit code is 0. Parse this because it returns bytes or none
        else:
            logger.warning("bash run returned an error")
            logger.info("stdout is: {}\n stderr is: {}".format(output[0], output[1]))
            return exit_code, output
