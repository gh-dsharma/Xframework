import pytest
from pathlib import Path

def workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates=None):

    #Given
    titanite = Titanite()
    if row_updates:
        replacement_row.update(row_updates)

    #When
    testcase_logger.info("Update precondition data")
    target_row = {'gene':'CSRM1'}
    target_file = titanite.cnv_path
    titanite.update_row_entry_in_tsv_file(target_file, target_row,  replacement_row)
    titanite.update_manifest_sha()

    testcase_logger.info("Generate input.json")
    titanite.generate_input_json()
    
    testcase_logger.info("Verify input.json exists")
    titanite.verify_input_json('sampleid', titanite.SAMPLEID) 
    
    testcase_logger.info("Run CSRM to produce output.json")
    titanite.run(titanite_container)

    testcase_logger.info("Get CSRM's output value")
    actual_value = titanite.get_output_value(titanite.MET)

    #Then
    testcase_logger.info("Verifying output.json's value is Detected or Not Detected")
    titanite.check_equal(actual_value, expected_value)

@pytest.mark.hamster_demo
@pytest.mark.intest
class Test_CNV:

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'MET' , 'call':2}, 'Detected'),
        ({'gene':'ME'  , 'call':2}, 'Not Detected'),
        ({'gene':'METT', 'call':2}, 'Not Detected'),
        ({'gene':'MMET', 'call':2}, 'Not Detected'),
        ({'gene':'EGFR'    , 'call':2}, 'Not Detected'),
        ({'gene':''    , 'call':2}, 'Not Detected'),
        ], ids=[
            'MET Detected'     , \
            'ME Not Detected'  , \
            'METT Not Detected', \
            'MMET Not Detected', \
            'EGFR Not Detected', \
            'None Not Detected'   
        ])
    def test_gene(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene 'MET' with call '2' is described as Value: "Detected". All other call values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated cnv_call.hdr.tsv with call = '2', and %gene% is parametrized.
            3) Map of %gene% and %call% and %value%:
                - MET  | 2 |     Detected
                - ME   | 2 | Not Detected
                - MET1 | 2 | Not Detected
                - MME  | 2 | Not Detected
                - EGFR | 2 | Not Detected
                - None | 2 | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Eligible MET Amplification", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)
        

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'MET', 'call': 2 }, 'Detected'     ),
        ({'gene':'MET', 'call': 3 }, 'Not Detected' ),
        ({'gene':'MET', 'call': 1 }, 'Not Detected' ),
        ({'gene':'MET', 'call': -2}, 'Not Detected' ),
        ({'gene':'MET', 'call': 0}, 'Not Detected' ),
        ], ids=[
            '2 Detected'        , \
            '3 Not Detected'    , \
            '1 Not Detected'    , \
            '-2 Not Detected'   , \
            'None Not Detected'  
        ])
    def test_call(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify gene 'MET' with call '2' is described as Value: "Detected". All other gene values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated cnv_call.hdr.tsv with gene = 'MET', and %call% is parametrized.
            3) Map of %gene% and %call% and %value%:
                - MET | 2    |     Detected
                - MET | 3    | Not Detected
                - MET | 1    | Not Detected
                - MET | -2   | Not Detected
                - MET | None | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Eligible MET Amplification", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'MET'  , 'call':2 }, 'Detected'     ),
        ({'gene':'CSRM' , 'call':2 }, 'Not Detected' ),
        ({'gene':'MET'  , 'call':3 }, 'Not Detected' ), 
        ], ids=[
            'baseline Detected'         , \
            'gene not MET Not Detected' , \
            'call not 2 Not Detected'          
        ])
    def test_requirement_combinations(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value):
        """
        Description:   
            Verify that MET mutations are described as Value: "Not Detected" in output.json when one of the following is false:
                - gene = 'MET'
                - call = '2'

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated cnv_call.hdr.tsv with %gene% and %call%  parametrized:
            3) Map of %gene% and %call% and %value%:
                - MET  | 2 |     Detected
                - CSRM | 2 | Not Detected
                - MET  | 3 | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Eligible MET Amplification", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)


    