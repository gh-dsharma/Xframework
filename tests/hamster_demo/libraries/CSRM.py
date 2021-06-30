import logging
import libraries.helper as helper
import libraries.framework.bip_files as bip_files
from pathlib import Path
import numpy


class CSRM:
    """
    Controls the CSRM instance that allows you to drive the test case.
    """
    
    def __init__(self, test_case_directory):
        """
            Creates an csrm instance for test case run. 
        :Args:
         - test_case_directory - directory with data where csrm points too. eg. ../tests/csrm/data/TC_TOPAZ_2
        """
        self.test_case_directory = Path(test_case_directory) 
        if self.test_case_directory == None:
            raise NameError('Empty Test Case Directory')
        self.logger = logging.getLogger(__name__) 
        self.logger.info('Initializing CSRM class with test case directory {}'.format(test_case_directory))

    def get_json(self, path_to_file: 'Path') -> 'json obj':
        """
        Get json files from the test case directory: tests/csrm/data/TC_TOPAZ_N
        Convert a file that ends in .json and return it as a python object.
        https://docs.python.org/3/library/json.html

        :Usage:
            input_json = csrm.get_json("input.json")
            manifest_json = csrm.get_json("/bolts/lcm/manifest.json")
        :Returns:
            A json obj
        """
        location = self.test_case_directory / path_to_file
        json_file = helper.json_helper.get_json_file(location)
        return json_file

    def get_json_value(self, json_file, search_expression):
        """
        Extract elements from a JSON obj
        jmespath: similar to xpath but for json. https://jmespath.org/tutorial.html

        :Usage:
            jmespath.search('foo.bar', {'foo': {'bar': 'baz'}})
            'baz'
        :Returns:
            json element: this can either be a string or a list depending on the query
        """
        return helper.json_helper.get_json_value(search_expression, json_file)

    def verify_input_json(self, search_expression, expected_value):
        """
        Assert an key,value pair is inside input.json.
        Asserts stop the script from continuing if the data is not present.

        :Usage:
            csrm.verify_input_json('cancertype', 'Breast Cancer')
        :Returns:
            None
        """
        input_json = "input.json"
        json_file = helper.json_helper.get_json_file(self.test_case_directory / input_json)
        value = helper.json_helper.get_json_value(search_expression, json_file)
        assert value == expected_value, "{} was not found in {}".format(expected_value, json_file)

    def verify_output_json(self, search_expression, expected_value):
        """
        Assert an key,value pair is inside output.json
        Asserts stop the script from continuing if the data is not present.

        :Usage:
            csrm.verify_output_json('results[0].name', 'ESR1 Mutations')
        :Returns:
            None
        """
        output_json = "output.json"
        json_file = helper.json_helper.get_json_file(self.test_case_directory / output_json)
        value = helper.json_helper.get_json_value(search_expression, json_file)
        assert value == expected_value, "{} was not found in output.json".format(value)
 
    def verify_entry_in_tsv_file(self, file_name, pairs):
        """
        Assert a row entry is present in the tsv/csv. 
        Usually to check if a gene or mutation is present in the bip file

        :Usage:
            snv_tsv = "A018661201.snv_call.hdr.tsv"
            key_value_list = [('gene', 'ESR1'), ('mut_aa', 'D313E'), ('call',0)]
            csrm.verify_entry_in_tsv_file(snv_tsv, key_value_list) 
        :Returns:
            bool: if an entry in the tsv/csv
        """
        dataframe = helper.pandas_helper.return_as_dataframe(self.test_case_directory / file_name)
        isFound = helper.pandas_helper.check_entry_in_dataframe(dataframe, pairs)
        assert isFound == True, "{} was not found in t{}".format(pairs, file_name)

    def return_row_entry_in_tsv_file(self, file_name, pairs):

        dataframe = helper.pandas_helper.return_as_dataframe(self.test_case_directory / file_name)
        return helper.pandas_helper.get_entry_in_dataframe(dataframe, pairs)

    def update_row_entry_in_tsv_file(self, target_file:'path', target_row:dict, replacement_row:dict):
        helper.pandas_helper.update_row_entry_in_tsv_file(target_file, target_row, replacement_row)
        
        #verify precondition was updated
        updated_param = replacement_row['gene']
        bash_command = "grep {} {} | tail -n 1".format(updated_param, target_file)
        output = helper.subprocess_helper.run(bash_command)
        assert updated_param in output

    def run(self, container):
        """
        Invoke the container 
        :Usage:
            csrm.run(csrm_container)
        :Returns:
            None. output.json is generated in the test directory
        """
        container_command = "/opt/conda/bin/python3 /app/run.py --input_dir {}".format(self.test_case_directory)
        helper.docker_helper.run(container, container_command)

    def check_equal(self, a, b):
        """
        Check if items a and b are equal
        Checks are like an assert but it can continue on failure. Normal asserts stop on failure. 

        :Usage:
            value = csrm.get_json_value(output_json, 'results[0].value')
            check.equal(value,'A')
        :Returns:
            None. Errors are thrown in log if failure
        """
        helper.check_helper.equal(a,b)



        

    