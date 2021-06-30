import pytest
import logging
import libraries.helper as helper
from .config import Config
import tests.api_demo.libraries.api_demo as api_demo
logger = logging.getLogger(__name__)



@pytest.fixture(scope="session")
def app_config(test_version): #Refer to top level conftest for test_version fixture
    cfg = Config(test_version)
    return cfg

@pytest.fixture(scope="session") #Place holder for project in test
def Emerald(app_config):
    return app_config.emerald_version

@pytest.fixture(scope="function")
def accession_generator(request):
    return api_demo.generate_accession_id()

    



