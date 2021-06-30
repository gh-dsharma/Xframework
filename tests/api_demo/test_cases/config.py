import tests.api_demo.libraries.api_demo as api_demo

#Place holder to edit config
class Config:
    def __init__(self, env):

        self.emerald_version = {
            'v1' : api_demo,
            #'v2' : acs_v2
        }[env]

        self.artifactory_url = {
            'v1' : 'docker.artifactory01.ghdna.io/csrm_emerald:1.0-RC1',
            #'v2' : 'docker.artifactory01.ghdna.io/csrm_emerald:1.0-RC1' 
        }[env]