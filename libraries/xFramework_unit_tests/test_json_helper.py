import pytest
import json
from pathlib import Path
from libraries.helper.json_helper import get_json_file, get_json_value, write_json_file, update_json_file

path_to_folder = Path(__file__).parent
default_test_json = {"test": "Hello from json"}


def reset_json_file(json_file_path):
    with open(str(json_file_path), 'w') as outfile:
        json.dump(default_test_json, outfile, indent=2)


def test_gid_204905_get_json_file():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    reset_json_file(test_json_path)
    test_json = get_json_file(test_json_path)
    assert test_json == default_test_json


def test_gid_204906_get_json_file_negative():
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
    with pytest.raises(Exception):
        get_json_file("/nonexistent_path")


def test_gid_204907_get_json_value():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    reset_json_file(test_json_path)
    json_object = get_json_file(test_json_path)
    get_json_value('test', json_object)


# We don't error handle if the key isn't found, just pass back None from jmespath
def test_gid_204908_get_json_value_negative():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    json_object = get_json_file(test_json_path)
    assert get_json_value('nonexistent_key', json_object) is None


# Reset the test json file and check the contents, write to it
# then check the contents, then reset the json file again
def test_gid_204909_write_json_file():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    reset_json_file(test_json_path)
    json_object = get_json_file(test_json_path)
    assert json_object == default_test_json

    json_object_write = {"test": "testing write_json_file()"}
    write_json_file(test_json_path, json_object_write)
    json_object = get_json_file(test_json_path)
    assert json_object == json_object_write

    reset_json_file(test_json_path)


def test_gid_204910_write_json_file_negative():
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
    test_json_path = path_to_folder / "nonexistent_folder/nonexistent_json.json"

    json_object_write = {"test": "testing write_json_file()"}
    with pytest.raises(Exception):
        write_json_file(test_json_path, json_object_write)


def test_gid_204911_update_json_file():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    reset_json_file(test_json_path)
    json_object = get_json_file(test_json_path)
    assert json_object == default_test_json

    update_json_file(test_json_path, "test", "testing update_json_file()")
    json_object = get_json_file(test_json_path)
    expected_json = default_test_json
    expected_json["test"] = "testing update_json_file()"
    assert json_object == expected_json

    reset_json_file(test_json_path)


# Error log for this one could be better, currently erroring out at the
# logger level instead of the at the Exception raise after the log
def test_gid_204912_update_json_file_negatives():
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
    test_json_path = path_to_folder / "unit_test_data/test_json.json"
    reset_json_file(test_json_path)
    json_object = get_json_file(test_json_path)
    assert json_object == default_test_json

    with pytest.raises(Exception):
        update_json_file(test_json_path, "nonexistent_key", "testing update_json_file()")
