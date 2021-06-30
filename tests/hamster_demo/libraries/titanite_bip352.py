from .CSRM import CSRM
import logging
import libraries.helper as helper
from pathlib import Path
import libraries.framework.bip_files as bip_files

class TitaniteConfig:
    #BIP files:
    TEST_CASE_DIRECTORY = Path(__file__).parent.parent / "data/general_352"
    SNV_FILENAME        =  "A027954801.snv_call.hdr.tsv"
    CNV_FILENAME        =  "bolts/csm/A027954801.cnv_call.hdr.tsv"
    GENE_NAME_MAPPING   = {
                            'MET': 'Eligible MET Amplification',
                            'BRAF':'Exclusion Criteria: BRAF V600 Mutation', 
                            'RAS':'Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation'
                          }
    MANIFEST_FILENAME   =  "manifest.boltons.json"
    SAMPLEID            =  'A027954801'
    MET                 =  "MET"
    BRAF                =  "BRAF"
    RAS                 =  "RAS"

    #CSRM artifactrs
    INPUT_JSON          = "input.json"
    OUTPUT_JSON         = "output.json"

    #parameters for BIP 3.5.2:
    BIPVERSION          = "3.5.2"
    BIP_CONFIG_FILENAME = "bip_config.json"
    STUDYVERSIONID      = "KGA_17v1"
    PANEL_VERSION       = "GH2.11"
    lcm_version         = "1.0"
    csm_version         = "1.0-RLS3"

    @property
    def snv_path(self):
        return self.test_case_directory / TitaniteConfig.SNV_FILENAME
    
    @property
    def cnv_path(self):
        return self.test_case_directory / TitaniteConfig.CNV_FILENAME

    @property
    def bip_config_path(self):
        return self.test_case_directory / TitaniteConfig.BIP_CONFIG_FILENAME
    
    @property
    def manifest_path(self):
        return self.test_case_directory / TitaniteConfig.MANIFEST_FILENAME

    @property
    def input_json_path(self):
        return self.test_case_directory / TitaniteConfig.INPUT_JSON

    @property
    def output_json_path(self):
        return self.test_case_directory / TitaniteConfig.OUTPUT_JSON


class Titanite_v1(CSRM, TitaniteConfig):
    """
    Controls the Topaz instance that allows you to drive the test case.
    """

    def __init__(self, test_case_directory=TitaniteConfig.TEST_CASE_DIRECTORY):
        """
            Creates an topaz instance for test case run. 
        :Args:
         - test_case_directory - directory with data where topaz points too. eg. ../tests/topaz/data/TC_TOPAZ_2
        """
        super().__init__(test_case_directory)
        self.test_case_directory = Path(test_case_directory) 
        if self.test_case_directory == None:
            raise NameError('Empty Test Case Directory')
        self.logger = logging.getLogger(__name__) 
        self.logger.info('Initializing Topaz with BIP 3.5.2 test case directory {}'.format(test_case_directory))

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
            "sampleid": TitaniteConfig.SAMPLEID,
            "biprunid": "200313_A00277_0260_BH3MW5DSXY",
            "bipoutdir": str(self.test_case_directory),
            "createddate": "2018-12-19T22:46:08.828Z",
            "product": "Guardant360 LDT",
            "csasversion": "v1.0-rc5-261-9bd0451",
            "studyversionid": TitaniteConfig.STUDYVERSIONID,
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

        #write the file
        helper.json_helper.write_json_file(self.input_json_path, copy_of_json_key_value_pairs)

    def get_output_value(self, gene_name):
        output_file_path = self.output_json_path
        output_json = super().get_json(output_file_path)
        jamespath_search_expression = "results[?name=='{}'].value".format(TitaniteConfig.GENE_NAME_MAPPING[gene_name])
        try:
            self.logger.info("returning json from {}".format(output_file_path))
            actual_value = super().get_json_value(output_json, jamespath_search_expression)
            return actual_value[0]
        except IndexError:
            return []

    def update_manifest_sha(self):
        file_paths = [self.snv_path, self.cnv_path]

        for path in file_paths:
            md5 = bip_files.get_md5sum(path)
            manifest_path = self.manifest_path
            if "bolts" in str(path): #"bolts/csm/A027954801.cnv_call.hdr.tsv"
                delimeter_to_get_filename = -3
                file_name = str(path).split('/')[delimeter_to_get_filename:]
            else:
                delimeter_to_get_filename = -1
                file_name = str(path).split('/')[delimeter_to_get_filename:]
            file_name = "/".join(file_name)
            bip_files.update_manifest_md5(manifest_path, file_name, md5, verbose=False)

    def update_bip_config(self, key, value):
        bip_config_path = self.bip_config_path
        helper.json_helper.update_json_file(bip_config_path, key, value, verbose=False)

        #verify updates were made
        json_obj = helper.json_helper.get_json_file(manifest_path)
        updated_value = helper.json_helper.get_json_value(jamespath_search_expression, json_obj)
        assert updated_value == value

    def update_manifest_boltons(self, jamespath_search_expression, value):
        manifest_path = self.manifest_path
        helper.json_helper.update_json_file(manifest_path, jamespath_search_expression, value, verbose=True)

        #verify updates were made
        json_obj = helper.json_helper.get_json_file(manifest_path)
        updated_value = helper.json_helper.get_json_value(jamespath_search_expression, json_obj)
        assert updated_value == value


        