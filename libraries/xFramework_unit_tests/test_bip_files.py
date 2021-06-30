from libraries.framework.bip_files import update_row_in_tsv, update_manifest_md5, get_md5sum
import libraries.helper as helper
from pathlib import Path
import pytest
import json

path_to_folder = Path(__file__).parent


def test_gid_204888_update_row_in_tsv():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    target_row = {'gene': 'CSRM1'}
    replacement_row = {'gene': 'replaced_gene'}
    tsv_path = path_to_folder / "unit_test_data/pandas_data.tsv"

    update_row_in_tsv(tsv_path, target_row, replacement_row)

    df = helper.pandas_helper.return_as_dataframe(tsv_path)
    assert helper.pandas_helper.check_entry_in_dataframe(df, replacement_row) == True

    # Update it back
    target_row = {'gene': 'replaced_gene'}
    replacement_row = {'gene': 'CSRM1'}
    update_row_in_tsv(tsv_path, target_row, replacement_row)


def test_gid_204889_update_row_in_tsv_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    target_row = {'gene': 'non existent row'}
    replacement_row = {'gene': 'replaced_gene'}
    tsv_path = path_to_folder / "unit_test_data/pandas_data.tsv"

    bash_command = "md5sum {}".format(tsv_path)
    original_md5sum = helper.subprocess_helper.run(bash_command)

    with pytest.raises(AssertionError):
        update_row_in_tsv(tsv_path, target_row, replacement_row)

    bash_command = "md5sum {}".format(tsv_path)
    new_md5sum = helper.subprocess_helper.run(bash_command)

    assert original_md5sum == new_md5sum


def test_gid_204890_update_manifest_md5():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    test_manifest_path = path_to_folder / "unit_test_data/test_manifest.json"
    test_json_file_name = "test_json.json"
    test_json_file_path = path_to_folder / "unit_test_data" / test_json_file_name

    # Standardize the test_json and get the new md5
    with open(str(test_json_file_path), 'w') as outfile:
        json.dump({"test": "Hello from json"}, outfile, indent=2)
    md5sum1 = get_md5sum(test_json_file_path)

    # Update the manifest with the md5 (don't use the
    # update_manifest_md5 since that's a separate unit test)
    with open(test_manifest_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data['elements'][0]['md5'] = md5sum1
    with open(test_manifest_path, "w") as jsonFile:
        json.dump(data, jsonFile)

    # Update the test_json and get the new md5
    with open(str(test_json_file_path), 'w') as outfile:
        json.dump({"test": "testing update_manifest_md5()"}, outfile, indent=2)
    md5sum2 = get_md5sum(test_json_file_path)

    # Update the manifest with the update_manifest_md5() function
    update_manifest_md5(test_manifest_path, test_json_file_name, md5sum2)

    # Verify the manifest was updated correctly
    with open(test_manifest_path, "r") as jsonFile:
        data = json.load(jsonFile)
    assert data['elements'][0]['md5'] == md5sum2


def test_gid_204891_update_manifest_md5_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    test_manifest_path = path_to_folder / "unit_test_data/test_manifest.json"
    test_json_file_name = "test_json.json"

    with pytest.raises(Exception):
        update_manifest_md5(test_manifest_path, "nonexistent_file.json", "abc")

    with pytest.raises(Exception):
        update_manifest_md5("nonexistent_path", test_json_file_name, "abc")


def test_gid_204892_get_md5sum():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    test_json_path = path_to_folder / "unit_test_data/pandas_data.tsv"
    test_json_md5 = get_md5sum(test_json_path)
    assert test_json_md5


def test_gid_204893_get_md5sum_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    test_json_path = path_to_folder / "unit_test_data/nonexistent_file"
    get_md5sum(test_json_path)
