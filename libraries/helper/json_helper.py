import json
import logging
import jmespath
import libraries.helper as helper

logger = logging.getLogger(__name__) #framework.libraries.helper

def get_json_file(path: str, mode: str = 'r', verbose=True) -> 'json obj':
    """
    Convert a file that ends in .json and return it as a python object.
    https://docs.python.org/3/library/json.html

    :Usage:
        json_file = helper.json_helper.get_json_file(test_case_directory / input_json)
        value = helper.json_helper.get_json_value(search_expression, json_file)
    :Returns:
        A python object
    """
    try:
        with open(path, mode) as input_file:
            input_json = json.load(input_file)
        if verbose:
            logger.info("{} is: {}".format(path, json.dumps(input_json, indent=2)))
        return input_json
    except:
        logger.error("Could not open json", exc_info=1)
        raise NameError

def get_json_value(jmespath_search_expression: str, json_obj: 'json obj', verbose=True) -> 'json element':
    """
    Extract elements from a JSON obj
    jmespath: similar to xpath but for json. https://jmespath.org/tutorial.html

    :Usage:
        json_file = helper.json_helper.get_json_file(test_case_directory / input_json)
        value = helper.json_helper.get_json_value(search_expression, json_file)
    :Returns:
        json element: this can either be a string or a list depending on the query
    :Notes:
        jmespath.search('foo.bar', {'foo': {'bar': 'baz'}})
        'baz'
    """
    value = jmespath.search(jmespath_search_expression, json_obj)
    if verbose:
        logger.info('Found {} using {} in {}'.format(value, jmespath_search_expression, json.dumps(json_obj, indent=2)))
    return value

def write_json_file(destination: 'Path to output.json', json_obj: 'obj'):
    """
    Write a json obj to a file.
    Wrapper for json.dump: https://docs.python.org/3/library/json.html

    :Usage:
        json = {'foo': {'bar': 'baz'}}
        output_file = str(test_case_directory / "output.json")
        helper.json_helper.write_json_file(output_file, json)
    :Returns:
        None
    """
    try:
        with open(str(destination), 'w') as outfile:
            json.dump(json_obj, outfile, indent=2)
        logger.info("generated {}. JSON: {}".format(destination,  json.dumps(json_obj, indent=2)))
    except:
        logger.error("Could not write to {}".format(destination), exc_info=1)
        raise NameError

def update_json_file(filepath: str, key_to_update: 'jmespath expression', new_value:str, verbose=True):
    """
    Updates existing json obj's values with a given key. 
    :Usage:
        See update_manifest_md5()
    :Returns:
    :Notes:
        Does not update globally
    """
    json_obj = helper.json_helper.get_json_file(path=filepath, verbose=verbose)
    search_results_filter = helper.json_helper.get_json_value(key_to_update, json_obj, verbose)

        #filter search results before sending to sed. we only want str or a list of length 1
    if type(search_results_filter) == str:
        search_results = search_results_filter
    elif type(search_results_filter) == list:
        if len(search_results_filter) == 1:
            search_results = search_results_filter[0]
        else:
            logger.error("search_results_filter is{}".format(search_results_filter))
            raise ValueError("More than 1 match, json update failed")
    else:
        raise ValueError("Unsupported type")

    logger.info("search results is: {}".format(search_results_filter))
    
    bash_replace_command = "sed -i 's/{}/{}/' {}".format(search_results, new_value, filepath)
    helper.subprocess_helper.run(bash_replace_command)
        

    

