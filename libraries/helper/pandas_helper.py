import logging
import pandas
import numpy
import libraries.helper as helper

logger = logging.getLogger(__name__) #framework.libraries.helper

def update_row_entry_in_tsv_file(tsv_path: 'path', target_row_entry:dict, replacement_row_entry:dict, strict=True):
    """
    Update an existing row in a tsv. 
    :Usage:
        target_row = {'gene': 'TOPAZ1'}
        replacement_row = [('gene', 'KEAP1'), ('mut_aa', 'G31A'), ('ldt_reportable',1), ('somatic_call', 'somatic')]
        topaz.update_row_entry_in_tsv_file(indel_path, target_row, replacement_row)
    :Returns:
        None
    :Notes:
        If strict option is true, there must be 1 and only 1 target row to be replaced. 
    """

    #get the row target row to be replaced:
            #this is a pandas row
            #we assert that it only matches 1 row
            #replace this row
    dataframe = return_as_dataframe(tsv_path)
    rows = get_entry_in_dataframe(dataframe, target_row_entry)
    rows_index = numpy.flatnonzero(rows)
    if strict:
        assert len(rows_index) == 1, "row index is {}".format(len(rows_index))

    #unpack the list for the replacement row before updating
    new_row_keys = list(replacement_row_entry.keys())
    new_row_values = list(replacement_row_entry.values())
    
    #update the row
    row_index = rows_index[0] #only update the first occurence
    dataframe.loc[row_index, new_row_keys] = new_row_values 
    dataframe.to_csv(tsv_path, sep = "\t", index=False)
    logger.info("Updating target row with {}".format(replacement_row_entry))

def return_as_dataframe(path: 'path') -> 'panda dataframe':
    """
    Get a csv/tsv as a Pandas dataframe
    :Usage:
        test_case_directory = Path(__file__).parent.parent / "data" / "TC_EMERALD_1c"
        dataframe = helper.pandas_helper.return_as_dataframe(test_case_directory / file_name)
    :Returns:
        a pandas dataframe
    """
    try:
        path_str = str(path.resolve())
        file_extension = path_str[-3:]
        if file_extension == 'tsv':
            df = pandas.read_csv(path_str, sep='\t', header=0) 
        elif file_extension == 'csv':
            df = pandas.read_csv(path_str, sep=',', header=0)
        df.name = path_str
        logger.info('Returning file as panda data frame {}'.format(path)) 
        return df
    except: 
        logger.error("Not csv or tsv", exc_info=1)
        raise Exception

def get_entry_in_dataframe(df: 'Pandas dataframe', key_value: dict) -> 'panda dataframe': 
    """
    Helper for update_row_entry_in_tsv_file()
    :Usage:
        N/A, use update_row_entry_in_tsv_file()
    :Returns:
        a pandas dataframe 
    """

    #Handle case when list is 0
    if not key_value:
        raise ValueError('Empty dictionary')

    #key, value = key_value[0] #don't use pop b/c it destroys the data for debugging
    keys = list(key_value.keys())
    values = list(key_value.values())

    #Handle the case when list is 1
    if len(keys) == 1:
        key = keys[0]
        value = values[0]
        logger.info('Found. Key, Value {} in {}: '.format(key_value, df.name))
        return (df[key] == value)

    #Handle the case when list > 1
    filtered = (df[keys[0]] == values[0]) #dummy head. 
    
    for key, value in key_value.items(): 
        filtered = filtered & (df[key] == value) #use dummy head as initial filter. 
        #This pattern used instead of filtered &= filtered. The latter one breaks check_entry_in_dataframe() on empty results
        if not filtered.any():
            logger.warning('Search chain stopped at Key: {} Value: {}. Actual is {}'.format(key, value, df.get(key)[0]))

    isFound = filtered.any()
    logger.info('{}. Key, Value {} in {}: '.format(isFound, key_value, df.name))

    return filtered 

def check_entry_in_dataframe(df: 'Pandas dataframe', key_value_list: list) -> bool:
    """
    Check for a row entry inside the dataframe. Return boolean if found or not.
    Solves the same problem as ((data_frame['gene'] == 'ESR1') & (data_frame['call'] == 0) &... ).any()
    :Usage:
        dataframe = self.helper.pandas_helper.return_as_dataframe(self.test_case_directory / file_name)
        isFound = self.helper.pandas_helper.check_entry_in_dataframe(dataframe, pairs)
        assert isFound == True, "{} was not found in t{}".format(pairs, file_name)
    :Returns:
        bool 
        
    """

    return get_entry_in_dataframe(df, key_value_list).any()