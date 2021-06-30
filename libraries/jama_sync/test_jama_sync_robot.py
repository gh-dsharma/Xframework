import jama_sync as jama_sync
from pathlib import Path
import pytest
from libraries.unit_test_helper import replace_section_in_file, standardize_file


testing = True
path_to_folder = str(Path(__file__).parent)
root_test_data_folder = path_to_folder + "/test_data/robot_jama_sync_test"
standard_file_path = path_to_folder + "/test_data/docs_standards/test_docs_standard.robot"


# Test that Jama Sync will accept correct documentation
def test_correct_documentation(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'robot' test cases were read:\n" \
           "<NEW>: Test Documentation" in output


def test_add(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--add"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'robot' test cases were read:\n" \
           "<NEW>: Test Documentation" in output
    assert "Successfully updated: TC-GID-" in output
    assert ": Test Documentation in project 'SANBOX_BI'" in output


# WARNING: this test case depends on the last test case
@pytest.mark.dependency(depends=["test_add"])
def test_add_update(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--update"])
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'robot' test cases were read:\nTC-GID-"
    assert "Successfully updated: TC-GID" in output
    assert ": Test Documentation in project 'SANBOX_BI'" in output


# WARNING: this test case depends on the last test case
@pytest.mark.dependency(depends=["test_add_update"])
@pytest.mark.parametrize("section, section_change",
                         [("...     Description:",
                           "    ...     Testing Jama Sync table writing in Description\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing |\n"
                           "    ...     testing | testing | testing |\n"
                           "    ...     *end table*"),
                          ("...     Prerequisites:",
                           "    ...     1) Testing Jama Sync table writing in Prerequisites\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     *end table*"),
                          ("...     Test Data:",
                           "    ...     1) Testing Jama Sync table writing in Test Data\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     *end table*"),
                          ]
                         )
def test_table_documentation_happy_path(capfd, username, password, section, section_change):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--update"])
    replace_section_in_file(root_test_data_folder + "/Automated/test_docs.robot", section, section_change, "robot")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'robot' test cases were read:\nTC-GID-"
    assert "Successfully updated: TC-GID" in output
    assert ": Test Documentation in project 'SANBOX_BI'" in output


@pytest.mark.parametrize("section, delete_section, expected_string",
                         [("...     Description:", True, "Expecting 'Description' line in test case <NEW>: Test "
                                                         "Documentation (if this section is present, check that it is "
                                                         "the first line in the doc-string)"),
                          ("...     Description:", False, "Expecting 'Prerequisites' line in test case <NEW>: "
                                                          "Test Documentation or the previous section data (if this "
                                                          "section is present, check that it is directly 2 lines "
                                                          "below the last section)"),
                          ("...     Prerequisites:", True, "Expecting 'Prerequisites' line in test case "
                                                           "<NEW>: Test Documentation or the previous section "
                                                           "data (if this section is present, check that it is "
                                                           "directly 2 lines below the last section)"),
                          ("...     Prerequisites:", False, "Failed to read test file: Expecting either '1)', "
                                                            "another dash '-', or '*begin table*' in the "
                                                            "Prerequisites section in <NEW>: Test Documentation"),
                          ("...     Test Data:", True, "Expecting 'Test Data' line in test case <NEW>: Test "
                                                       "Documentation or the previous section data (if this "
                                                       "section is present, check that it is directly 2 lines "
                                                       "below the last section)"),
                          ("...     Test Data:", False, "Failed to read test file: Expecting either '1)', "
                                                        "another dash '-', or '*begin table*' in the Test Data "
                                                        "section in <NEW>: Test Documentation"),
                          ("...     Steps:", True, "Expecting 'Steps' line in test case <NEW>: Test Documentation "
                                                   "or the previous section data (if this section is present, "
                                                   "check that it is directly 2 lines below the last section)"),
                          ("...     Steps:", False, "Expecting '1)' line under 'Steps' in test case "
                                                    "<NEW>: Test Documentation"),
                          ]
                         )
def test_basic_incorrect_documentation(capfd, username, password, section, delete_section, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--add"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    replace_section_in_file(root_test_data_folder + "/Automated/test_docs.robot", section, "", "robot",
                            delete_section=delete_section)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section_change, expected_string",
                         [("    ...     1) Testing Jama Sync writing in Steps\n"
                           "    ...         Notes: Testing Jama Sync writing in Notes",
                           "Expecting 'ER:' line under 'Steps' in test case <NEW>: Test Documentation"),
                          ("    ...     1) Testing Jama Sync writing in Steps\n"
                           "    ...         ER: Testing Jama Sync writing in Expected Results",
                           "Expecting 'Notes:' line under 'Steps' in test case <NEW>: Test Documentation"),
                          ]
                         )
def test_incorrect_steps_documentation(capfd, username, password, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--add"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    replace_section_in_file(root_test_data_folder + "/Automated/test_docs.robot", "...     Steps:",
                            section_change, "robot")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section, section_change, expected_string",
                         [("...     Prerequisites:",
                           "    ...     1) Testing Jama Sync writing in Prerequisites\n"
                           "    ...     3) Testing Jama Sync writing in Prerequisites\n",
                           "Expecting either '2)', another dash '-', or '*begin table*' in the "
                           "Prerequisites section in <NEW>: Test Documentation"),
                          ("...     Test Data:",
                           "    ...     1) Testing Jama Sync writing in Test Data\n"
                           "    ...     3) Testing Jama Sync writing in Test Data\n",
                           "Expecting either '2)', another dash '-', or '*begin table*' in the "
                           "Test Data section in <NEW>: Test Documentation"),
                          ("...     Steps:",
                           "    ...     1) Testing Jama Sync writing in Steps\n"
                           "    ...         ER: Testing Jama Sync writing in Expected Results\n"
                           "    ...         Notes: Testing Jama Sync writing in Notes\n"
                           "    ...     3) Testing Jama Sync writing in Steps\n",
                           "Expecting '2)' line under 'Steps' in test case <NEW>: Test Documentation"),
                          ]
                         )
def test_incorrect_numbering_documentation(capfd, username, password, section, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--add"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    replace_section_in_file(root_test_data_folder + "/Automated/test_docs.robot", section, section_change, "robot")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section, section_change, expected_string",
                         [("...     Description:",
                           "    ...     Testing Jama Sync table writing in Description\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n"
                           "    ...     *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in <NEW>: Test Documentation"),
                          ("...     Description:",
                           "    ...     Testing Jama Sync table writing in Description\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n",
                           "Expecting '*end table*' in the Description section in <NEW>: Test Documentation"),
                          ("...     Prerequisites:",
                           "    ...     1) Testing Jama Sync table writing in Prerequisites\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n"
                           "    ...     *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in <NEW>: Test Documentation"),
                          ("...     Prerequisites:",
                           "    ...     1) Testing Jama Sync table writing in Prerequisites\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n",
                           "Expecting '*end table*' in the Prerequisites section in <NEW>: Test Documentation"),
                          ("...     Test Data:",
                           "    ...     1) Testing Jama Sync table writing in Test Data\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n"
                           "    ...     *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in <NEW>: Test Documentation"),
                          ("...     Test Data:",
                           "    ...     1) Testing Jama Sync table writing in Test Data\n"
                           "    ...     *begin table*\n"
                           "    ...     testing | testing | testing\n"
                           "    ...     testing | testing\n",
                           "Expecting '*end table*' in the Test Data section in <NEW>: Test Documentation"),
                          ]
                         )
def test_incorrect_table_documentation(capfd, username, password, section, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", root_test_data_folder + "/Automated/test_docs.robot",
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "robot", "--add"])
    standardize_file(root_test_data_folder + "/Automated/test_docs.robot", standard_file_path)
    replace_section_in_file(root_test_data_folder + "/Automated/test_docs.robot", section, section_change, "robot")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output
