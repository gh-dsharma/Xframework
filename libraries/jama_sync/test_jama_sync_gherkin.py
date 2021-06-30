import jama_sync as jama_sync

import pytest

from pathlib import Path

from libraries.unit_test_helper import replace_section_in_file, standardize_file

testing = True
path_to_folder = str(Path(__file__).parent)
root_test_data_folder = path_to_folder + "/test_data/gherkin_jama_sync_test"
test_path = f"{root_test_data_folder}/test_docs.feature"
standard_file_path = path_to_folder + "/test_data/docs_standards/test_docs_standard.feature"


# Test that Jama Sync will accept correct documentation
def test_correct_documentation(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin"])
    standardize_file(test_path, standard_file_path)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'gherkin' test cases were read:\n" \
           "test_NEW docs" in output


def test_add(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--add"])
    standardize_file(test_path, standard_file_path)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'gherkin' test cases were read:\n" \
           "test_NEW docs" in output
    assert "Successfully updated: test_gid_" in output


# WARNING: this test case depends on the last test case
@pytest.mark.dependency(depends=["test_add"])
def test_add_update(capfd, username, password):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--update"])
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'gherkin' test cases were read:\ntest_" in output and "docs" in output


# WARNING: this test case depends on the last test case
@pytest.mark.dependency(depends=["test_add_update"])
@pytest.mark.parametrize("section, section_change",
                         [("Description:",
                           "        Testing Jama Sync table writing in Description\n"
                           "        *begin table*\n"
                           "        testing | testing | testing |\n"
                           "        testing | testing | testing |\n"
                           "        *end table*"),
                          ("Prerequisites:",
                           "        1) Testing Jama Sync table writing in Prerequisites\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing | testing\n"
                           "        *end table*"),
                          ("Test Data:",
                           "        1) Testing Jama Sync table writing in Test Data\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing | testing\n"
                           "        *end table*"),
                          ]
                         )
def test_table_documentation_happy_path(capfd, username, password, section, section_change):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--update"])
    replace_section_in_file(test_path, section, section_change, "gherkin")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    assert "the following 'gherkin' test cases were read:\ntest_" in output and "docs" in output


@pytest.mark.parametrize("section, delete_section, expected_string",
                         [("Description:", True, "Expecting 'Description' line in test case test_NEW docs "
                                                 "(if this section is present, check that it is the first line "
                                                 "in the doc-string)"),
                          ("Description:", False, "Expecting 'Prerequisites' line in test case test_NEW docs or the "
                                                  "previous section data (if this section is present, check that it "
                                                  "is directly 2 lines below the last section)"),
                          ("Prerequisites:", True, "Expecting 'Prerequisites' line in test case test_NEW docs or the "
                                                   "previous section data (if this section is present, check that it "
                                                   "is directly 2 lines below the last section)"),
                          ("Prerequisites:", False, "Failed to read test file: Expecting either '1)', another dash "
                                                    "'-', or '*begin table*' in the Prerequisites section in "
                                                    "test_NEW docs"),
                          ("Test Data:", True, "Expecting 'Test Data' line in test case test_NEW docs or the "
                                               "previous section data (if this section is present, check that it "
                                               "is directly 2 lines below the last section)"),
                          ("Test Data:", False, "Failed to read test file: Expecting either '1)', another dash '-', or"
                                                " '*begin table*' in the Test Data section in test_NEW docs"),
                          ("Steps:", True, "Expecting 'Steps' line in test case test_NEW docs or the previous section "
                                           "data (if this section is present, check that it is directly 2 lines below "
                                           "the last section)"),
                          ("Steps:", False, "Expecting '1)' line under 'Steps' in test case test_NEW docs"),
                          ]
                         )
def test_basic_incorrect_documentation(capfd, username, password, section, delete_section, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--add"])
    standardize_file(test_path, standard_file_path)
    replace_section_in_file(test_path, section, "", "gherkin", delete_section=delete_section)
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section_change, expected_string",
                         [("        1) Testing Jama Sync writing in Steps\n"
                           "            Notes: Testing Jama Sync writing in Notes",
                           "Expecting 'ER:' line under 'Steps' in test case test_NEW docs"),
                          ("        1) Testing Jama Sync writing in Steps\n"
                           "            ER: Testing Jama Sync writing in Expected Results",
                           "Expecting 'Notes:' line under 'Steps' in test case test_NEW docs"),
                          ]
                         )
def test_incorrect_steps_documentation(capfd, username, password, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--add"])
    standardize_file(test_path, standard_file_path)
    replace_section_in_file(test_path, "Steps:", section_change, "gherkin")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section, section_change, expected_string",
                         [("Prerequisites:",
                           "        1) Testing Jama Sync writing in Prerequisites\n"
                           "        3) Testing Jama Sync writing in Prerequisites\n",
                           "Expecting either '2)', another dash '-', or '*begin table*' in the "
                           "Prerequisites section in test_NEW docs"),
                          ("Test Data:",
                           "        1) Testing Jama Sync writing in Test Data\n"
                           "        3) Testing Jama Sync writing in Test Data\n",
                           "Expecting either '2)', another dash '-', or '*begin table*' in the "
                           "Test Data section in test_NEW docs"),
                          ("Steps:",
                           "        1) Testing Jama Sync writing in Steps\n"
                           "            ER: Testing Jama Sync writing in Expected Results\n"
                           "            Notes: Testing Jama Sync writing in Notes\n"
                           "        3) Testing Jama Sync writing in Steps\n",
                           "Expecting '2)' line under 'Steps' in test case test_NEW docs"),
                          ]
                         )
def test_incorrect_numbering_documentation(capfd, username, password, section, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--add"])
    standardize_file(test_path, standard_file_path)
    replace_section_in_file(test_path, section, section_change, "gherkin")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output


@pytest.mark.parametrize("section, section_change, expected_string",
                         [("Description:",
                           "        Testing Jama Sync table writing in Description\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n"
                           "        *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in test_NEW docs"),
                          ("Description:",
                           "        Testing Jama Sync table writing in Description\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n",
                           "Expecting '*end table*' in the Description section in test_NEW docs"),
                          ("Prerequisites:",
                           "        1) Testing Jama Sync table writing in Prerequisites\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n"
                           "        *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in test_NEW docs"),
                          ("Prerequisites:",
                           "        1) Testing Jama Sync table writing in Prerequisites\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n",
                           "Expecting '*end table*' in the Prerequisites section in test_NEW docs"),
                          ("Test Data:",
                           "        1) Testing Jama Sync table writing in Test Data\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n"
                           "        *end table*",
                           "Table row: 'testing | testing' does not have the expected amount of columns:3 as the rest "
                           "of the table in test_NEW docs"),
                          ("Test Data:",
                           "        1) Testing Jama Sync table writing in Test Data\n"
                           "        *begin table*\n"
                           "        testing | testing | testing\n"
                           "        testing | testing\n",
                           "Expecting '*end table*' in the Test Data section in test_NEW docs"),
                          ]
                         )
def test_incorrect_table_documentation(capfd, username, password, section, section_change, expected_string):
    arguments = jama_sync.parse_args(["-root_path", root_test_data_folder,
                                      "-test_path", test_path,
                                      "-jama_user", username, "-jama_pass", password,
                                      "-interpreter", "gherkin", "--add"])
    standardize_file(test_path, standard_file_path)
    replace_section_in_file(test_path, section, section_change, "gherkin")
    jama_sync.update_jama(arguments, testing)
    output, err = capfd.readouterr()
    if expected_string not in output:
        print(output)
    assert expected_string in output
