import pytest
from pathlib import Path
import libraries.helper as helper
import libraries.framework.bip_files as bip_files

def workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates=None):

    #Given
    titanite = Titanite()
    if row_updates:
        replacement_row.update(row_updates)

    #When
    testcase_logger.info("Update precondition data")
    target_row = {'gene':'CSRM1'}
    target_file = titanite.snv_path
    titanite.update_row_entry_in_tsv_file(target_file, target_row,  replacement_row)
    titanite.update_manifest_sha()

    testcase_logger.info("Generate input.json")
    titanite.generate_input_json()
    
    testcase_logger.info("Verify input.json exists")
    titanite.verify_input_json('sampleid', titanite.SAMPLEID) 
    
    testcase_logger.info("Run CSRM to produce output.json")
    titanite.run(titanite_container)

    testcase_logger.info("Get CSRM's output value")
    actual_value = titanite.get_output_value(titanite.BRAF)

    #Then
    testcase_logger.info("Verifying output.json's value is Detected or Not Detected")
    titanite.check_equal(actual_value, expected_value)

@pytest.mark.hamster_demo
class Test_SNV:

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'BRAF'  , 'call':1, 'mut_aa': 'V600A'}, 'Detected'     ),
        ({'gene':'BRA'   , 'call':1, 'mut_aa': 'V600A'}, 'Not Detected' ),
        ({'gene':'BRAFF' , 'call':1, 'mut_aa': 'V600A'}, 'Not Detected' ),
        ({'gene':''      , 'call':1, 'mut_aa': 'V600A'}, 'Not Detected' ),
        ], ids=[
            'BRAF Detected'     , \
            'BRA Not Detected'  , \
            'BRAFF Not Detected', \
            'None Not Detected'   
        ])
    def test_gene(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene BRAF missense mutations are described as Value: "Detected". All other gene values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: call = '1', codon = 600 and mut_aa is not synonymous or nonsense and %gene% is parametrized.
            3) Map of %gene% and %value%:
                - BRAF  |     Detected
                - BRA   | Not Detected
                - BRAFF | Not Detected
                - None  | Not Detected
                
        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: BRAF V600 Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)
        

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600A'}, 'Detected' ),
        ({'gene':'BRAF' , 'call':0 , 'mut_aa': 'V600A'}, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':-1, 'mut_aa': 'V600A'}, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':'', 'mut_aa': 'V600A'}, 'Not Detected' ),
        ], ids=[
            '1 Detected'        , \
            '0 Not Detected'    , \
            '-1 Not Detected'   , \
            'None Not Detected'   
        ])
    def test_call(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene BRAF missense mutations with call = 1 are described as Value: "Detected". All other call values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'BRAF', codon = 600 and mut_aa is not synonymous or nonsense and %call% is parametrized.
            3) Map of %call% and %value%:
                - 1    |     Detected
                - 0    | Not Detected
                - -1   | Not Detected
                - None | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: BRAF V600 Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600A'}, 'Detected'     ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V599A'}, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V601A'}, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'GA'   }, 'Not Detected' ),
        ], ids=[
            '600 Detected'      , \
            '599 Not Detected'  , \
            '601 Not Detected'  , \
            'None Not Detected'   
        ])
    def test_mut_aa_codon(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene BRAF missense mutations in codon 600 are described as Value: "Detected". All other codon values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'BRAF', call = 1, mut_aa is not synonymous or nonsense and codon is parametrized.
            3) Map of %codon% and %value%:
                - 600  |     Detected
                - 599  | Not Detected
                - 601  | Not Detected
                - None | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: BRAF V600 Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600A' }, 'Detected'     ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600V' }, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600*' }, 'Not Detected' ),
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': ''      }, 'Not Detected' ),
        ], ids=[
            'missense Detected'       , \
            'synonymous Not Detected' , \
            'nonsense Not Detected'   , \
            'Null Not Detected'   
        ])
    def test_mut_aa_type(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene BRAF missense mutations are described as Value: "Detected". All synonymous or nonsense are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'BRAF', call = 1, mut_aa is parametrized.
            3) Map of %mut_aa% and %value% :
                - V600A  |     Detected
                - V600V  | Not Detected
                - V600*  | Not Detected
                - None   | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: BRAF V600 Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600A' }, 'Detected'     ), #happy path
        ({'gene':'CSRM' , 'call':1 , 'mut_aa': 'V600A' }, 'Not Detected' ), #gene not BRAF
        ({'gene':'BRAF' , 'call':0 , 'mut_aa': 'V600A' }, 'Not Detected' ), #call not 1
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V601A' }, 'Not Detected' ), #codon not 600
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600V' }, 'Not Detected' ), #synonymous mutation
        ({'gene':'BRAF' , 'call':1 , 'mut_aa': 'V600*' }, 'Not Detected' ), #nonsense mutation
        ], ids=[
            'baseline Detected'                , \
            'gene not BRAF Not Detected'       , \
            'call not 1 Not Detected'          , \
            'codon not 600 Not Detected'       , \
            'synonymous mutation Not Detected' , \
            'nonsense mutation Not Detected'   
        ])
    def test_requirement_combinations(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify that BRAF missense mutations are described as Value: "Not Detected" in output.json when one of the following is false:
                - gene = 'BRAF'
                - call = '1'
                - codon = 600
                - mut_aa is not synonymous or nonsense

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with  gene, call and mut_aa parametrized.
            3) Map of %gene%, %call%, %mut_aa% and %value% :
                - BRAF | 1 | 'V600A' |     Detected
                - EGFR | 1 | 'V600A' | Not Detected
                - BRAF | 0 | 'V600A' | Not Detected
                - BRAF | 1 | 'V601A' | Not Detected
                - BRAF | 1 | 'V600V' | Not Detected
                - BRAF | 1 | 'V600*' | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: BRAF V600 Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)

    