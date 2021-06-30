import logging
from pathlib import Path
import libraries.helper as helper
logger = logging.getLogger(__name__) #framework.libraries.helper

def update_row_in_tsv(tsv_path: 'path', target_row_entry:dict, replacement_row_entry:dict):
    helper.pandas_helper.update_row_entry_in_tsv_file(tsv_path, target_row_entry, replacement_row_entry)

def update_manifest_md5(manifest_path: str, file_name:str, new_md5: str, verbose=False) : # TODO group all md5 functions into seperate module
    """
    Updates manifest md5 in place 

    :Usage:
        manifest_path = Path(__file__name).parent / "data/TC_EMERAMD_2/manifest.json"
        manifest_path = manifest_path.resolve() #Convert to literal string
        # literal_manifest_path = "/ghds/groups/bip_sqa/personal_spaces/pco/pytest_framework/tests/emerald/data/TC_EMERALD_2/manifest.json"
        file_name =  "A018659601.short.bwamem.cram"
        bip_files.update_manifest_md5(manifest_path, file_name, "abc")
    :Returns:
        None
    :Example manifest.json:
        {
            "category": "full_bam", 
            "send_report": false, 
            "file_name": "A018659601.short.bwamem.cram", 
            "sample": "A018659601", 
            "volatile": false, 
            "file_size": 1822332837, 
            "flowcell": "190810_NB551235_0267_AH72H7BGXB", 
            "md5": "abc"
        }
    """
    jamespath_search_expression = "elements[?file_name=='{}'].md5".format(file_name)
    helper.json_helper.update_json_file(manifest_path, jamespath_search_expression, new_md5, verbose)

def get_md5sum(filepath: str) -> str: 
    """
    Returns the md5 of the file. 
    Emerald doesn't run if md5 doesn't match the md5 in manifest.bolt.json

    :Usage:
        snv_location = test_case_directory / snv_tsv
        snv_md5 = emerald.get_md5sum(snv_location)
    :Returns:
        str: md5sum 
    """
    bash_command_for_md5 = "md5sum {} | cut -d ' ' -f1".format(str(filepath))
    md5sum = helper.subprocess_helper.run(bash_command_for_md5)
    return md5sum
