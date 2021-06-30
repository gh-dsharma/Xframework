import libraries.helper as helper
from pathlib import Path
import pandas
import pytest


def test_gid_204914_return_as_dataframe_tsv():
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
    tsv_path = Path(__file__).parent / "unit_test_data/pandas_data.tsv"
    df = helper.pandas_helper.return_as_dataframe(tsv_path)
    assert isinstance(df, pandas.DataFrame)


def test_gid_204915_return_as_dataframe_csv():
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
    csv_path = Path(__file__).parent / "unit_test_data/pandas_data.csv"
    df = helper.pandas_helper.return_as_dataframe(csv_path)
    assert isinstance(df, pandas.DataFrame)


def test_gid_204916_return_as_dataframe_exception():
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
    py_path = Path(__file__)
    with pytest.raises(Exception):
        df = helper.pandas_helper.return_as_dataframe(py_path)


def test_gid_204917_check_entry_in_dataframe_true():
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
    tsv_path = Path(__file__).parent / "unit_test_data/pandas_data.tsv"
    df = helper.pandas_helper.return_as_dataframe(tsv_path)
    assert helper.pandas_helper.check_entry_in_dataframe(df, target_row) == True


def test_gid_204918_check_entry_in_dataframe_false():
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
    target_row = {'gene': 'doesnotexists'}
    tsv_path = Path(__file__).parent / "unit_test_data/pandas_data.tsv"
    df = helper.pandas_helper.return_as_dataframe(tsv_path)
    assert helper.pandas_helper.check_entry_in_dataframe(df, target_row) == False


def test_gid_204919_get_entry_in_dataframe():
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
    # This is just a helper method and for test_update_row_entry_in_tsv_file and not called directly
    pass


def test_gid_204920_update_row_entry_in_tsv_file_fail():
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
    tsv_path = Path(__file__).parent / "unit_test_data/pandas_data.tsv"

    bash_command = "md5sum {}".format(tsv_path)
    original_md5sum = helper.subprocess_helper.run(bash_command)

    with pytest.raises(AssertionError):
        helper.pandas_helper.update_row_entry_in_tsv_file(tsv_path, target_row, replacement_row)

    bash_command = "md5sum {}".format(tsv_path)
    new_md5sum = helper.subprocess_helper.run(bash_command)

    assert original_md5sum == new_md5sum


def test_gid_204921_update_row_entry_in_tsv_file_success():
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
    tsv_path = Path(__file__).parent / "unit_test_data/pandas_data.tsv"

    helper.pandas_helper.update_row_entry_in_tsv_file(tsv_path, target_row, replacement_row)

    df = helper.pandas_helper.return_as_dataframe(tsv_path)
    assert helper.pandas_helper.check_entry_in_dataframe(df, replacement_row) == True

    # Update it back
    target_row = {'gene': 'replaced_gene'}
    replacement_row = {'gene': 'CSRM1'}
    helper.pandas_helper.update_row_entry_in_tsv_file(tsv_path, target_row, replacement_row)

