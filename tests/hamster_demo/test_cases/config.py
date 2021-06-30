from tests.hamster_demo.libraries.titanite_bip352 import Titanite_v1
from tests.hamster_demo.libraries.titanite_bip353 import Titanite_v2

class Config:
    def __init__(self, env):

        self.csrm_version = {
            'v1' : Titanite_v1, #This uses BIP 3.5.2
            'v2' : Titanite_v2  #This uses BIP 3.5.3
        }[env]

        self.artifactory_url = {
            'v1' : 'docker.artifactory01.ghdna.io/csrm_titanite:1.0.0-RC2',
            'v2' : 'docker.artifactory01.ghdna.io/csrm_titanite:1.0.0-RC2'
        }[env]

        self.docker_volumes = {'Opt' : {'bind': '/opt/tests/csrm/data/', 'mode': 'rw'}} #Edits here should reflfect in the dockerfile

        self.build_version = {
            'v1' : 'v1.0.0-RC2-38-76132b1',
            'v2' : 'v1.0.0-RC2-38-76132b1' 
        }[env]