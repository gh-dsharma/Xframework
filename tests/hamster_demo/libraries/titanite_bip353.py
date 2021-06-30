from .titanite_bip352 import Titanite_v1
import logging
import libraries.helper as helper
from pathlib import Path

class Titanite_v2(Titanite_v1):

    #BIP files:
    TEST_CASE_DIRECTORY = Path(__file__).parent.parent / "data/general_353"
    SNV_FILENAME        =  "A023637101.snv_call.hdr.tsv"
    CNV_FILENAME        =  "bolts/csm/A023637101.cnv_call.hdr.tsv"
    SAMPLEID            =  'A023637101'
    MANIFEST_FILENAME   =  "manifest.boltons.json"

    #parameters for BIP 3.5.2:
    BIPVERSION          = "3.5.3"
    BIP_CONFIG_FILENAME = "bip_config.json"
    STUDYVERSIONID      = "KGA_17v1"
    PANEL_VERSION       = "GH2.11"
    lcm_version         = "1.0"
    csm_version         = "1.0-RLS3"
    
    def __init__(self, test_case_directory=TEST_CASE_DIRECTORY):
        super().__init__(test_case_directory)
        self.version = "Topaz with BIP 3.5.3"
        self.logger = logging.getLogger(__name__) 
        self.logger.info('Initializing Topaz V2 with BIP 3.5.3 with test case directory {}'.format(test_case_directory))

    @property
    def snv_path(self):
        return self.test_case_directory / Titanite_v2.SNV_FILENAME
    
    @property
    def cnv_path(self):
        return self.test_case_directory / Titanite_v2.CNV_FILENAME

    @property
    def bip_config_path(self):
        return self.test_case_directory / Titanite_v2.BIP_CONFIG_FILENAME
    
    @property
    def manifest_path(self):
        return self.test_case_directory / Titanite_v2.MANIFEST_FILENAME

    def generate_input_json(self, json_key_value_pairs: dict = None) -> 'input.json':
        """
        Generate's input.json in the test case directory. 
        :Usage:
            topaz.generate_input_json()                     #Generates with default values
            topaz.generate_input_json({"cancertype":'Liver'}) #Generates with default values and cancer type as Liver
        :Returns:
            None. input.json is generated in the test directory
        """
        #default input_json_template
        input_json_template = {
            "requestid": "A0194938",
            "sampleid": Titanite_v2.SAMPLEID,
            "biprunid": "200313_A00277_0260_BH3MW5DSXY",
            "bipoutdir": str(self.test_case_directory),
            "createddate": "2018-12-19T22:46:08.828Z",
            "product": "Guardant360 LDT",
            "csasversion": "v1.0-rc5-261-9bd0451",
            "studyversionid": Titanite_v2.STUDYVERSIONID,
            "callbackurl": {
                "authurl": "http://lims/connections/",
                "dataurl": "http://lims/iuo_result_response"
            },
            "dockercmd": "/opt/conda/bin/python3 /app/run.py --input_dir",
            "imagepath": "docker.artifactory01.ghdna.io/csrm_topaz:master_latest",
            "samplestatus": "PASS"
        }
        
        if json_key_value_pairs == None:
            json_key_value_pairs = {}

        #pass default values for missing key value pairs
        copy_of_json_key_value_pairs = json_key_value_pairs #create a copy and do not edit the original input

        for key, value in input_json_template.items():
            if copy_of_json_key_value_pairs.get(key) == None:
                copy_of_json_key_value_pairs[key] = value

        #outputfile
        input_file_path = str(self.test_case_directory / "input.json")
        helper.json_helper.write_json_file(input_file_path, copy_of_json_key_value_pairs)
    
    def print_version(self):
        print(self.version)
        