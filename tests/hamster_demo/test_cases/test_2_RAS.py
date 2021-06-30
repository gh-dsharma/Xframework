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
    actual_value = titanite.get_output_value(titanite.RAS)

    #Then
    testcase_logger.info("Verifying output.json's value is Detected or Not Detected")
    titanite.check_equal(actual_value, expected_value)

@pytest.mark.hamster_demo
class Test_SNV:

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'KRAS' , 'call':1, 'mut_aa': 'G12A'}, 'Detected'     ),
        ({'gene':'NRAS' , 'call':1, 'mut_aa': 'G12A'}, 'Detected'     ),
        ({'gene':'KRA'  , 'call':1, 'mut_aa': 'G12A'}, 'Not Detected' ),
        ({'gene':'NRA'  , 'call':1, 'mut_aa': 'G12A'}, 'Not Detected' ),
        ({'gene':'RAS'  , 'call':1, 'mut_aa': 'G12A'}, 'Not Detected' ),
        ({'gene':''     , 'call':1, 'mut_aa': 'G12A'}, 'Not Detected' ),
        ], ids=[
            'KRAS Detected'     , \
            'NRAS Detected'     , \
            'KRA Not Detected'  , \
            'NRA Not Detected', \
            'RAS Not Detected', \
            'None not detected'  
        ])
    def test_gene(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates=None):
        """
        Description:   
            Verify RAS missense mutations are described as Value: "Detected". All other gene values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: call = '1', codon = 12 and mut_aa is not synonymous or nonsense and %gene% is parametrized.
            3) Map of %gene% and %value%:
                - KRAS |     Detected
                - NRAS |     Detected
                - KRA  | Not Detected
                - NRA  | Not Detected
                - RAS  | Not Detected
                - None | Not Detected
                
        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value)
        

    @pytest.mark.parametrize('row_updates',
        [
        ({'gene':'KRAS'}),
        ({'gene':'NRAS'})
        ], ids=[
            'KRAS', \
            'NRAS'
        ])
    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G12A'}, 'Detected' ),
        ({'gene':'RAS' , 'call':0 , 'mut_aa': 'G12A'}, 'Not Detected' ),
        ({'gene':'RAS' , 'call':-1, 'mut_aa': 'G12A'}, 'Not Detected' ),
        ({'gene':'RAS' , 'call':'', 'mut_aa': 'G12A'}, 'Not Detected' ),
        ], ids=[
            '1 Detected'        , \
            '0 Not Detected'    , \
            '-1 Not Detected'   , \
            'None Not Detected'   
        ])
    def test_call(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates):
        """
        Description:   
            Verify RAS missense mutations with call = 1 are described as Value: "Detected". All other call values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'KRAS' or 'NRAS', codon = 12 and mut_aa is not synonymous or nonsense and %call% is parametrized.
            3) Map of %call% and %value%:
                - KRAS | 1    |     Detected 
                - KRAS | 0    | Not Detected 
                - KRAS | -1   | Not Detected 
                - KRAS | None | Not Detected 
                - NRAS | 1    |     Detected 
                - NRAS | 0    | Not Detected 
                - NRAS | -1   | Not Detected 
                - NRAS | None | Not Detected 

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates)

    @pytest.mark.parametrize('row_updates',
        [
        ({'gene':'KRAS'}),
        ({'gene':'NRAS'})
        ], ids=[
            'KRAS', \
            'NRAS'
        ])
    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G12A'  }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G13A'  }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G59A'  }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G61A'  }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G117A' }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G146A' }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G11A'  }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G14A'  }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G58A'  }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G60A'  }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G62A'  }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G116A' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G118A' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G145A' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G147A' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'GA'    }, 'Not Detected' ),
        ], ids=[
            'G12A Detected'      ,\
            'G13A Detected'      ,\
            'G59A Detected'      ,\
            'G61A Detected'      ,\
            'G117A Detected'     ,\
            'G146A Detected'     ,\
            'G11A Not Detected'  ,\
            'G14A Not Detected'  ,\
            'G58A Not Detected'  ,\
            'G60A Not Detected'  ,\
            'G62A Not Detected'  ,\
            'G116A Not Detected' ,\
            'G118A Not Detected' ,\
            'G145A Not Detected' ,\
            'G147A Not Detected' ,\
            'GA   Not Detected'  
        ])
    def test_mut_aa_codon(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates):
        """
        Description:   
            Verify RAS missense mutations in codons 12, 13, 59, 61, 117, 146 are described as Value: "Detected". All other codon values are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'KRAS' or 'NRAS', call = 1, mut_aa is not synonymous or nonsense and codon is parametrized.
            3) Map of %codon% and %value%:
                - KRAS | G12A  |     Detected
                - KRAS | G13A  |     Detected
                - KRAS | G59A  |     Detected
                - KRAS | G61A  |     Detected
                - KRAS | G117A |     Detected
                - KRAS | G146A |     Detected
                - KRAS | G11A  | Not Detected
                - KRAS | G14A  | Not Detected
                - KRAS | G58A  | Not Detected
                - KRAS | G60A  | Not Detected
                - KRAS | G62A  | Not Detected
                - KRAS | G116A | Not Detected
                - KRAS | G118A | Not Detected
                - KRAS | G145A | Not Detected
                - KRAS | G147A | Not Detected
                - KRAS | GA    | Not Detected
                - NRAS | G12A  |     Detected
                - NRAS | G13A  |     Detected
                - NRAS | G59A  |     Detected
                - NRAS | G61A  |     Detected
                - NRAS | G117A |     Detected
                - NRAS | G146A |     Detected
                - NRAS | G11A  | Not Detected
                - NRAS | G14A  | Not Detected
                - NRAS | G58A  | Not Detected
                - NRAS | G60A  | Not Detected
                - NRAS | G62A  | Not Detected
                - NRAS | G116A | Not Detected
                - NRAS | G118A | Not Detected
                - NRAS | G145A | Not Detected
                - NRAS | G147A | Not Detected
                - NRAS | GA    | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates)

    @pytest.mark.parametrize('row_updates',
        [
        ({'gene':'KRAS'}),
        ({'gene':'NRAS'})
        ], ids=[
            'KRAS', \
            'NRAS'
        ])
    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G12A' }, 'Detected'     ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G12G' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': 'G12*' }, 'Not Detected' ),
        ({'gene':'RAS' , 'call':1 , 'mut_aa': ''     }, 'Not Detected' ),
        ], ids=[
            'missense Detected'       , \
            'synonymous Not Detected' , \
            'nonsense Not Detected'   , \
            'Null Not Detected'   
        ])
    def test_mut_aa_type(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates):
        """
        Description:   
            Verify gene RAS missense mutations are described as Value: "Detected". All synonymous or nonsense are "Not Detected"

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with: gene = 'KRAS' or 'NRAS', call = 1, mut_aa is parametrized.
            3) Map of %mut_aa% and %value% :
                - KRAS | G12A  |     Detected
                - KRAS | G12G  | Not Detected
                - KRAS | G12*  | Not Detected
                - KRAS | None  | Not Detected
                - NRAS | G12A  |     Detected
                - NRAS | G12G  | Not Detected
                - NRAS | G12*  | Not Detected
                - NRAS | None  | Not Detected

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates)

    @pytest.mark.parametrize('replacement_row, expected_value',
        [
        ({'gene':'KRAS' , 'call':1 , 'mut_aa': 'G12A' }, 'Detected'     ), #happy path
        ({'gene':'NRAS' , 'call':1 , 'mut_aa': 'G12A' }, 'Detected'     ), #happy path
        ({'gene':'CSRM' , 'call':1 , 'mut_aa': 'G12A' }, 'Not Detected' ), #gene not KRAS
        ({'gene':'KRAS' , 'call':0 , 'mut_aa': 'G12A' }, 'Not Detected' ), #KRAS & call not 1
        ({'gene':'KRAS' , 'call':1 , 'mut_aa': 'G11A' }, 'Not Detected' ), #KRAS & incorrect codon
        ({'gene':'KRAS' , 'call':1 , 'mut_aa': 'G12G' }, 'Not Detected' ), #KRAS & synonymous mutation
        ({'gene':'KRAS' , 'call':1 , 'mut_aa': 'G12*' }, 'Not Detected' ), #KRAS & nonsense mutation
        ({'gene':'NRAS' , 'call':0 , 'mut_aa': 'G12A' }, 'Not Detected' ), #NRAS & call not 1
        ({'gene':'NRAS' , 'call':1 , 'mut_aa': 'G11A' }, 'Not Detected' ), #NRAS & incorrect codon
        ({'gene':'NRAS' , 'call':1 , 'mut_aa': 'G12G' }, 'Not Detected' ), #NRAS & synonymous mutation
        ({'gene':'NRAS' , 'call':1 , 'mut_aa': 'G12*' }, 'Not Detected' ), #NRAS & nonsense mutation
        ], ids=[
            'baseline KRAS - Detected'                  , \
            'baseline NRAS - Detected'                  , \
            'gene not KRAS or NRAS - Not Detected'      , \
            'KRAS & call not 1 - Not Detected'          , \
            'KRAS & incorrect codon -  Not Detected'    , \
            'KRAS & synonymous mutation - Not Detected' , \
            'KRAS & nonsense mutation - Not Detected'   , \
            'NRAS & call not 1 - Not Detected'          , \
            'NRAS & incorrect codon -  Not Detected'    , \
            'NRAS & synonymous mutation - Not Detected' , \
            'NRAS & nonsense mutation - Not Detected'   , \
        ])
    def test_requirement_combinations(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates=None):
        """
        Description:   
            Verify that RAS missense mutations are described as Value: "Not Detected" in output.json when one of the following is false:
                - gene = 'KRAS' or 'NRAS'
                - call = '1'
                - codon is either 12, 13, 59, 61, 117 or 146
                - mut_aa is not synonymous or nonsense

        Prerequisites:
            1) CSRM-Titanite docker image with the correct version is available
            2) Generated snv_call.hdr.tsv with  gene, call and mut_aa parametrized.
            3) Map of %gene%, %call%, %mut_aa% %value% and comments :
                - KRAS | 1 | 'G12A' |     Detected | happy path KRAS
                - NRAS | 1 | 'G12A' |     Detected | happy path NRAS
                - CSRM | 1 | 'G12A' | Not Detected | gene not KRAS
                - KRAS | 0 | 'G12A' | Not Detected | KRAS & call not 1
                - KRAS | 1 | 'G11A' | Not Detected | KRAS & incorrect codon
                - KRAS | 1 | 'G12G' | Not Detected | KRAS & synonymous mutation
                - KRAS | 1 | 'G12*' | Not Detected | KRAS & nonsense mutation
                - NRAS | 0 | 'G12A' | Not Detected | NRAS & call not 1
                - NRAS | 1 | 'G11A' | Not Detected | NRAS & incorrect codon
                - NRAS | 1 | 'G12G' | Not Detected | NRAS & synonymous mutation
                - NRAS | 1 | 'G12*' | Not Detected | NRAS & nonsense mutation

        Test Data: NA

        Steps:
            1) Run CSRM-Titanite with input files
                ER: Output.json is generated
                Notes: NA
            2) Check the content of the output.json file
                ER: The following key and value pairs exist in output.json:
                    - {["results"][{"Name": "Exclusion Criteria: KRAS/NRAS (codons 12, 13, 59, 61, 117, 146) Mutation", "Value": %expected_value%}]}
                Notes: NA

        Projects: Clinical Study Analysis and Reporting Platform
        """
        workflow(self, testcase_logger, Titanite, titanite_container, general_dataset, replacement_row, expected_value, row_updates)

    