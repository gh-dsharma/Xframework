#!/usr/bin/env python
# content of jama_sync.py

import argparse
import io
import json
import sys
import traceback

from pathlib import Path
from typing import Dict, List, Tuple

from libraries.doc_read_helper import read_section, read_step_section
from libraries.interperter import GherkinInterpreter, Interpreter, InterpreterFactory, PytestInterpreter, \
    RobotInterpreter
from libraries.jama_api import JamaClientHelper
from libraries.test_case import TestCase


VALID_INTERPRETERS = ['xframework', 'robot', 'gherkin']

config_path = Path(__file__).parent / 'config.json'
with open(config_path, 'r') as file:
    config = json.load(file)

# TODO: Add an exception handler for the situation where test cases are being added but the root folder is
#  not found in the jama projects that they belong to. Currently the cases are added to the master project
#  (BIP Master) but they dont get added to the applicable projects and thus do not receive GIDs
#  in their respective pytest files. What should happen is that the tool looks for the root folders
#  in the Jama Projects first


def initialize_jama_client(jama_username: str, jama_password: str) -> JamaClientHelper:
    """
    Return an initialized JamaClientHelper

    Args:
        jama_username: Username for the Jama client
        jama_password: Password for the Jama client

    Returns:
        An initialized Jama client
    """
    return JamaClientHelper(config['jama_url'], jama_username, jama_password,
                            config['default_test_case_api_type'],
                            config['default_folder_api_type'],
                            config['default_api_status'],
                            config['default_test_case_status'])


def parse_args(args: List[str]):
    """
cls
pytest
    Return an ArgumentParser object containing the arguments passed in

    Args:
        args: A list of arguments to be parsed

    Returns:
        An ArgumentParser object containing the arguments passed in
    """
    parser = argparse.ArgumentParser(description='update Jama test cases based upon a provided test file path')
    parser.add_argument("-root_path", help="path to the root folder of all test cases that map to Jama", required=True)
    parser.add_argument("-test_path", help="path to a test file or directory that contains test files", required=True)
    parser.add_argument("-jama_user", help="username (client ID) for current Jama REST API user", required=True)
    parser.add_argument("-jama_pass", help="password (client secret) for current Jama REST API user", required=True)
    parser.add_argument("-interpreter", help="interpreter used to read test files", type=str,
                        choices=VALID_INTERPRETERS, required=True)
    parser.add_argument("--update", help="update a test case", default=False, action="store_true")
    parser.add_argument("--add", help="add a test case", default=False, action="store_true")

    args_return = parser.parse_args(args)
    args_return.root_jama_folder_path = format_path(args_return.root_path)
    args_return.test_file = format_path(args_return.test_path)
    return args_return


def format_path(file_path: str) -> str:
    """
    Return a formatted file path in order to remove illegal characters and format a path in case of user errors

    Args:
        file_path: A file path string

    Returns:
        A file path that is formatted without illegal characters and without a backslash in the front of the path
    """
    # The illegal characters are the following: [’, ‘, “, ”] which are formatted quotes which
    # are not the same type of quotes that can be read within a path
    list_of_illegal_path_chars = [chr(8216), chr(8217), chr(8220), chr(8221)]
    for i in list_of_illegal_path_chars:
        file_path = file_path.replace(i, "")

    # The path should not start with a back slash if this is a relative path
    if not Path(file_path).exists():
        if file_path.startswith("/"):
            raise OSError("The path '" + file_path + "' does not exist. If you are entering a "
                          "relative path, make sure the path does not start with a '/'")
        else:
            raise OSError("The path '" + file_path + "' does not exist.")
    return file_path


def read_test_cases(test_cases_section: str, parent_folder_path: str, args, interpreter: Interpreter
                    ) -> Tuple[List[TestCase], List[TestCase]]:
    """
    Iterate through the test cases section and check that all test cases have required documentation
    information before returning the information as TestCase objects

    Args:
        test_cases_section: A string containing the test cases section of a test file
        parent_folder_path: A string representing the path from the parent folder to a file
        args: Arguments passed in from the command line
        interpreter: the interpreter used to interpret the test case section

    Returns:
        An array of TestCase objects representing all test case information that was passed in
    """
    test_case_section = False
    update_test_case_list = []
    add_test_case_list = []
    buf = io.StringIO(test_cases_section)
    line = buf.readline()

    while line:
        update_tc = False
        line = line.strip()

        if args.add:
            if line.startswith(interpreter.add_test_case_start_string):
                test_case_section = True

        if args.update:
            if line.startswith(interpreter.update_test_case_start_string):
                update_tc = True
                test_case_section = True

        # This is for testing purposes, documentation testing
        if not args.update and not args.add:
            if line.startswith(interpreter.add_test_case_start_string):
                test_case_section = True
            elif line.startswith(interpreter.update_test_case_start_string):
                update_tc = True
                test_case_section = True

        if test_case_section:
            if isinstance(interpreter, PytestInterpreter):
                new_test_case_name = \
                    line[line.find(interpreter.test_case_indicator) +
                         len(interpreter.test_case_indicator):line.rfind("(")]

                # Initialize test case by the test case name
                new_test_case = TestCase(new_test_case_name, parent_folder_path)

                # Initialize the test case's global ID
                if update_tc:
                    global_id = "gid_" + new_test_case.get_name().strip("test_gid_").split("_")[0]
                    new_test_case.set_global_id(global_id)
                else:
                    new_test_case.set_global_id("NEW")

                # Case to handle the situation where the declaration of a test case goes
                # on to the next line because the line exceeds the character limit
                while not line.strip().endswith("):"):
                    line = buf.readline().strip()

                # Check that the documentation immediately begins after test case declaration
                documentation_start = buf.readline()
                if '"""' not in documentation_start:
                    raise Exception('Expecting immediate documentation start -"""- coming after the test case name '
                                    'in test case ' + new_test_case.get_name())
            elif isinstance(interpreter, RobotInterpreter):
                # Initialize test case by the test case name
                new_test_case = TestCase(line.strip(), parent_folder_path)

                # Check that there is a documentation section
                if "[Documentation]" not in buf.readline():
                    raise Exception("Expecting '[Documentation]' line under test case " + new_test_case.get_name())

                # Initialize the test case's global ID
                if update_tc:
                    global_id = new_test_case.get_name()[new_test_case.get_name().find("TC-") +
                                                         len("TC-"):new_test_case.get_name().find(":")]
                    new_test_case.set_global_id(global_id)
                else:
                    new_test_case.set_global_id("<NEW>")
            elif isinstance(interpreter, GherkinInterpreter):
                new_test_case_name = \
                    line[line.find(interpreter.test_case_indicator) + len(interpreter.test_case_indicator):]
                print(new_test_case_name)

                # Initialize test case by the test case name
                new_test_case = TestCase(new_test_case_name, parent_folder_path)

                # Initialize the test case's global ID
                if update_tc:
                    global_id = "gid_" + new_test_case.get_name().strip("test_gid_").split("_")[0]
                    new_test_case.set_global_id(global_id)
                else:
                    new_test_case.set_global_id("NEW")

                # Check that the documentation immediately begins after test case declaration
                documentation_start = buf.readline()
                if '"""' not in documentation_start:
                    raise Exception('Expecting immediate documentation start -"""- coming after the test case name '
                                    'in test case ' + new_test_case.get_name())

            # Read in description information and ensure that the information is documented correctly
            description = read_section(buf, new_test_case, "Description")
            new_test_case.set_description(description)

            # Read in Prerequisite information and ensure that the information is documented correctly
            prerequisites = read_section(buf, new_test_case, "Prerequisites")
            new_test_case.set_prerequisites(prerequisites)

            # Read in Test Data information and ensure that the information is documented correctly
            test_data = read_section(buf, new_test_case, "Test Data")
            new_test_case.set_test_data(test_data)

            # Read in Steps information and ensure that the information is documented correctly
            test_steps_line = buf.readline()
            if "Steps:" not in test_steps_line:
                raise Exception("Expecting 'Steps' line in test case " + new_test_case.get_name() +
                                " or the previous section data (if this section is present, check that it is "
                                "directly 2 lines below the last section)")

            count = 1
            line = buf.readline().strip()
            while line != "":

                # Read in step and ensure that it's numbered correctly
                count, line, step_description = read_step_section(buf, count, line, new_test_case, "Steps")

                # Read in expected result
                count, line, expected_result = read_step_section(buf, count, line, new_test_case, "ER")

                # Read in notes
                count, line, notes = read_step_section(buf, count, line, new_test_case, "Notes")

                new_test_case.add_step(step_description, expected_result, notes)

            # Read in Projects (scope) information and ensure that the information is documented correctly
            project_scope = buf.readline().strip()
            if "Projects:" not in project_scope:
                raise Exception("Expecting 'Projects:' line in test case " + new_test_case.get_name())
            project_scope = project_scope.replace("Projects:", "").strip()

            # Handy way of taking out white space in a list and splitting by ','
            projects = [x.strip() for x in project_scope.split(',')]

            # Warn the user that they are only adding a test case to the master default project if that is the case,
            # otherwise, Add the default master project for every test case as a default
            if [config['default_master_project']] == projects and isinstance(interpreter, RobotInterpreter):
                print("\nWARNING: you are ONLY adding test case " + new_test_case.get_name() +
                      " to the master default project:", config['default_master_project'])
            else:
                new_test_case.add_project(config['default_master_project'])

            for project in projects:
                if project == 'NA' or project == '':
                    raise Exception("'Projects:' line in test case needs at least one project: " +
                                    new_test_case.get_name())
                elif project not in config['jama_project_list']:
                    raise Exception("'Projects:' line has a project '" + project + "' that is not in the "
                                    "list of acceptable jama projects (reference the config.json file) : "
                                    + new_test_case.get_name())
                new_test_case.add_project(project.strip())

            if update_tc:
                update_test_case_list.append(new_test_case)
            else:
                add_test_case_list.append(new_test_case)

            test_case_section = False

        line = buf.readline()

    return add_test_case_list, update_test_case_list


def get_parent_folder_path(root_jama_folder_path: str, file_path: str) -> str:
    """
    Returns a path from the parent folder to the file

    Args:
        root_jama_folder_path: A string representing the path to the root of a Jama folder
        file_path: A string representing the path to a file

    Returns:
        A string representing the path from the parent folder to the file
    """
    # Get the folder (last item) and check that it's in the file path
    root_folder = root_jama_folder_path.split("/")[-1]

    if root_folder not in file_path:
        raise OSError("The root folder '" + root_folder + "' was not found in path '" +
                      file_path + "' The path must follow the root folder")
    else:
        parent_path = file_path[file_path.find(root_folder):]
        return parent_path


def read_file(args, file_path: str, interpreter: Interpreter) -> Tuple[List[TestCase], List[TestCase]]:
    """
    Read test cases in a given test file and return a
    list of test cases that were interpreted properly

    Args:
        args: Arguments passed in from the command line
        file_path: A string representing the path to the test file
        interpreter: the interpreter used to read

    Returns:
        A tuple of TestCase object lists that contain test cases from the test file
    """
    test_case_section = interpreter.filter_test_case_file(file_path)

    parent_folder_path = get_parent_folder_path(args.root_jama_folder_path, file_path)

    # Split and filter the test cases in the test cases section
    add_test_case_list, update_test_case_list = read_test_cases(test_case_section, parent_folder_path,
                                                                args, interpreter)

    print("\nFrom " + file_path + ", the following '" + interpreter.name + "' test cases were read:")
    print_all_test_case_names(add_test_case_list, False)
    print_all_test_case_names(update_test_case_list, False)
    print()

    return add_test_case_list, update_test_case_list


def check_sync(test_case: TestCase, jama_client: JamaClientHelper) -> bool:
    """
    Check that all test cases that are synced (link) are also synchronized (updates pushed)

    Args:
        test_case: A TestCase object
        jama_client: A JamaClientHelper object to call the Jama REST API

    Returns:
        A boolean that indicates whether the test case is synced (push) across all respective projects
    """

    # Get the master project test case id
    test_case_id = test_case.get_test_case_id(config['default_master_project'])

    # Get all items that are synced (link) to this parent test case
    synced_items = jama_client.get_synced_items(test_case_id)

    # If there was a problem getting the synced items, return False
    if not synced_items:
        return False

    # iterate through the synced (link) items and check if the items are synced (push)
    is_synced = True
    for item in synced_items:
        if jama_client.get_synced_items_status(test_case_id, item['id'])['inSync'] != -1:
            # Shouldn't be having multiple of the same test case in one project
            if test_case.get_project_name(item['project']) == config['default_master_project']:
                print("Warning: there are two of the same test cases in the project " +
                      config['default_master_project'] + ", we should not have two test cases in this project")

            print("'" + item['fields']['name'] + "' in project '" +
                  test_case.get_project_name(item['project']) + "' is in sync with " +
                  config['default_master_project'])
        else:
            print("'" + item['fields']['name'] + "' in project '" +
                  test_case.get_project_name(item['project']) + "' IS NOT IN SYNC WITH " +
                  config['default_master_project'])
            is_synced = False

    return is_synced


def check_all_test_cases_synced(test_case_list: List[TestCase], jama_client: JamaClientHelper) -> bool:
    """
    Check that all test cases in a given list are synced (pushed)
    with their test cases across their respective projects

    Args:
        test_case_list: An array of TestCase objects
        jama_client: A JamaClientHelper object to call the Jama REST API

    Returns:
        A boolean that indicates whether the test cases are synced (push) across all respective projects
    """
    for test_case in test_case_list:
        if not check_sync(test_case, jama_client):
            return False

    return True


def print_all_test_cases(test_case_list: List[TestCase]) -> None:
    """
    Iterate through the test case list and print out ALL information for each test case (For debugging)

    Args:
        test_case_list: An array of TestCase objects

    Returns:
        None
    """
    for test_case in test_case_list:
        print(test_case)


def print_all_test_case_names(test_case_list: List[TestCase], print_projects: bool) -> None:
    """
    Iterate through the test case list and print the names of each test case (and project if indicated)

    Args:
        test_case_list: An array of TestCase objects
        print_projects: A boolean that indicates whether projects should also be added

    Returns:
        None
    """
    for test_case in test_case_list:
        print(test_case.get_name())
        if print_projects:
            for project, project_track in test_case.get_projects().items():
                if hasattr(project_track, 'test_case_id'):
                    print("    " + project)
                else:
                    print("    * New Sync (Link) * ---> " + project)


def pull_project_tracking(test_case_list: List[TestCase], jama_client: JamaClientHelper) -> List[TestCase]:
    """
    Fill out all project track ids for a given list of test cases

    Args:
        test_case_list: An array of TestCase objects
        jama_client: A JamaClientHelper object to call the Jama REST API

    Returns:
        An array of updated TestCase objects containing all respective project tracking information
    """
    # Iterate through the test case's projects and obtain the project
    # ids and test case ids for each. We need to keep track of all test
    # case ids in case we need to sync (push)
    known_project_ids = {}
    for test_case in test_case_list:
        for project, value in test_case.get_projects().items():
            # If we already know the project id for a project, we should add it from known
            # project ids list. This keeps us from calling the API multiple times for the same project.
            if project in known_project_ids:
                project_id = known_project_ids[project]
            # If we don't know the project id, we get it from the API and add it to the known project id list.
            else:
                project_id = jama_client.get_project_id(project)
                known_project_ids[project] = project_id

            # Retrieve the test case id for that specified project, if there
            # is no project, tell the user that a new sync will be made
            test_case_id = jama_client.get_test_case_id_from_global_id(project, project_id, test_case.get_global_id())
            if test_case_id == -1:
                parent_id = jama_client.get_folder_id(project_id, test_case.get_parent_folder_path(), project)
                test_case.add_project_track(project, project_id, None, parent_id)
            else:
                test_case.add_project_track(project, project_id, test_case_id, jama_client.get_parent_id(test_case_id))

    return test_case_list


def sync_push_updates(test_case_list: List[TestCase], jama_client: JamaClientHelper) -> int:
    """
    Push all updated test cases to all projects that are synced (linked)

    Args:
        test_case_list: An array of TestCase objects
        jama_client: A JamaClientHelper object to call the Jama REST API

    Returns:
        An integer that indicates whether the test cases were
        updated and synced (push) across all respective projects
    """
    # If the user chooses, iterate through each test case and their respective project tracks.
    # For all project tracks (the projects they belong to) update their respective test cases
    # and check that the callback returns a success response. If there is no test case id for
    # the project, that means the test case needs to be added to a project
    print()
    for test_case in test_case_list:
        # If the user is trying to push updates for a test case with a GID
        # that does not exist in the master project, that means it doesn't exist,
        # so this needs to stop them from trying to proceed.
        if not test_case.get_test_case_id(config['default_master_project']):
            print("\nUnable to find test case " + test_case.get_name() + " in master project '" +
                  config['default_master_project'] + "' please make sure this test case "
                  "exists there before updating\n")
            continue

        for project, project_track in test_case.get_projects().items():
            if test_case.get_test_case_id(project) is None:
                default_test_case_id = test_case.get_test_case_id(config['default_master_project'])
                if jama_client.add_sync_link(project, test_case, default_test_case_id) >= 0:
                    print("Successfully synced (link): " + test_case.name + " to project '" + project + "'")
                else:
                    print("Failed to sync (link) properly: " + test_case.name + " to project '" + project + "'")
                    print("     If a test case called " + test_case.name + " was added in project '" + project +
                          "', please manually delete it")
            else:
                api_callback = jama_client.update_test_case(project, test_case)
                if 200 <= api_callback < 300:
                    print("Successfully updated: " + test_case.get_name() + " in project '" + project + "'")
                else:
                    print("Failed to upload:" + test_case.get_name() + ": Exited with status code:" +
                          api_callback + "\n")
    print()

    # Check that all test cases are actually in sync after the update
    if not check_all_test_cases_synced(test_case_list, jama_client):
        print("Not all test cases have been synced properly. "
              "(if you had test cases that only uploaded to the master jama project, ignore this) ")
        return -1

    return 0


def prompt_user_add_update(test_case_list: List[TestCase], add_update: str) -> List[TestCase]:
    """
    Prompt the user with the test case list and allow them to choose what test cases
    they want in the list of cases that will be added/updated

    Args:
        test_case_list: An array of TestCase objects
        add_update: A string representing whether the user is adding or updating

    Returns:
        A test case list that contains the selected test cases
    """
    test_case_list_is_ready = False

    # Keep prompting the user with the list of test cases that will be updated. If they do not want
    # the current list of test cases, prompt them with the option to add individual test cases. Only
    # exit if the user has declined to the both the current list of test cases and to the offer of
    # adding individual test cases
    while not test_case_list_is_ready:
        if add_update == "add":
            print("\nAre you sure you want to ADD the following test cases WITH THE FOLLOWING PROJECTS? :")
        else:
            print("\nAre you sure you want to UPDATE the following test cases WITH THE FOLLOWING PROJECTS? :")
        print("---------------------------------------------------------------------------------------")
        print_all_test_case_names(test_case_list, True)
        print("---------------------------------------------------------------------------------------\n")

        if add_update == "add":
            if input("Enter 'yes' to proceed with adding the test cases: ").strip() != "yes":
                if input("Enter 'yes' if you would still like to add one "
                         "or more cases from the list: ").strip() == "yes":
                    for test_case in test_case_list[:]:  # [:] - iterate through a copy of test_case_list
                        print("\n" + test_case.get_name())
                        if input("Enter 'yes' if you would like to update the test case above: ").strip() != "yes":
                            test_case_list.remove(test_case)
                else:
                    print("\nUser has refused to proceed")
                    return []
            else:
                test_case_list_is_ready = True
        elif add_update == "update":
            if input("Enter 'yes' to proceed with the update: ").strip() != "yes":
                if input("Enter 'yes' if you would still like to update one "
                         "or more cases from the list: ").strip() == "yes":
                    for test_case in test_case_list[:]:  # [:] - iterate through a copy of test_case_list
                        print("\n" + test_case.get_name())
                        if input("Enter 'yes' if you would like to update the test case above: ").strip() != "yes":
                            test_case_list.remove(test_case)
                else:
                    print("\nUser has refused to proceed")
                    return []
            else:
                test_case_list_is_ready = True

    return test_case_list


def add_new_test_cases(test_case_list: List[TestCase], jama_client: JamaClientHelper, interpreter: Interpreter
                       ) -> Tuple[List[TestCase], Dict]:
    """
    Add the test cases from the test case list to the default master project.

    Args:
        test_case_list: An array of TestCase objects
        jama_client: A JamaClientHelper object to call the Jama REST API
        interpreter: the interpreter used to modify test case titles

    Returns:
        A tuple containing the test case list and a dictionary of old and new test case names
    """
    new_name_dict = {}
    master_project_id = jama_client.get_project_id(config['default_master_project'])

    # Iterate through the test cases, add a new test cases in the default
    # master project and update them with their GID in the test case name
    for test_case in test_case_list:
        try:
            # Get the parent id and create new test case
            parent_id = jama_client.get_folder_id(master_project_id, test_case.get_parent_folder_path(),
                                                  config['default_master_project'])
            new_case_id = jama_client.add_new_test_case(config['default_master_project'], parent_id, test_case)

            # Modify test case titles depending on the interpreter
            if isinstance(interpreter, PytestInterpreter):
                new_global_id = jama_client.get_global_id(new_case_id).lower().replace("-", "_")
                old_name = test_case.get_name()
                new_name = test_case.get_name().replace("test_NEW", "test_" + new_global_id)
            elif isinstance(interpreter, RobotInterpreter):
                new_global_id = jama_client.get_global_id(new_case_id)
                old_name = test_case.get_name()
                new_name = test_case.get_name().replace("<NEW>", "TC-" + new_global_id)
            elif isinstance(interpreter, GherkinInterpreter):
                new_global_id = jama_client.get_global_id(new_case_id).lower().replace("-", "_")
                old_name = test_case.get_name()
                new_name = test_case.get_name().replace("test_NEW", "test_" + new_global_id)

            # Initialize test case information
            test_case_path = test_case.get_parent_folder_path()
            if test_case_path not in new_name_dict:
                new_name_dict[test_case_path] = {}
            new_name_dict[test_case_path][old_name] = new_name
            test_case.set_name(new_name)
            test_case.set_global_id(new_global_id)
            test_case.add_project_track(config['default_master_project'], master_project_id, new_case_id, parent_id)

            # Update the new test case with the updated name (with global id)
            jama_client.update_test_case(config['default_master_project'], test_case)
            print("Successfully added new test case: " + test_case.name +
                  " to project '" + config['default_master_project'] + "'")
        except Exception as e:
            print("Failed to add new test case properly: " + test_case.name +
                  " to project '" + config['default_master_project'] + "'")
            print("If a test case called " + test_case.name +
                  " was added in project '" + config['default_master_project'] +
                  "', please manually delete it")
            print("\nError while adding: " + str(e) + "\n")

    return test_case_list, new_name_dict


def update_jama(args, testing: bool = False) -> int:
    """
    Read a file, pull the Jama test case information across projects, then push the updates

    Args:
        args: Arguments passed in from the command line
        testing: A boolean that indicates whether the function is being used for testing,
                 if there is testing going on, we will skip the user prompt for now

    Returns:
        An integer that indicates whether the Jama update was successful or not
    """
    # TODO: implement input testing and remove the testing boolean

    if not args.add and not args.update and not testing:
        raise Exception("No add/update chosen. Please provide either a --add or --update option in the command")

    # Initialize the Jama client to add
    jama_client = initialize_jama_client(args.jama_user, args.jama_pass)

    # Create the interpreter
    interpreter = InterpreterFactory.create(args.interpreter, args.test_file)

    test_files = interpreter.get_test_files()

    try:
        # Add the test cases in each test file if we are adding/updating by directory
        if test_files:
            add_test_case_list = []
            update_test_case_list = []
            for test_file in test_files:
                add_list, update_list = read_file(args, test_file, interpreter)
                add_test_case_list.extend(add_list)
                update_test_case_list.extend(update_list)
        # Add the test cases in the single test file if we are not adding/updating by directory
        else:
            add_test_case_list, update_test_case_list = read_file(args, args.test_file, interpreter)

    except Exception as e:
        print("\nFailed to read test file: " + str(e) + "\n")
        print(traceback.format_exc())
        return -1

    add_status = 0
    update_status = 0

    # Stop the user from proceeding if they are attempting to add/update more than 30 cases
    if len(add_test_case_list) + len(update_test_case_list) > 30:
        raise Exception("Attempting to add/update more than 30 test cases at once, "
                        "please limit the scope to less test cases")

    # If the user chooses to add, prompt the user for the test cases that they will be adding,
    # add them to the main jama project, sync push the name and project scope updates,
    # then rewrite the test files with the updated global ids
    if args.add and add_test_case_list:
        try:
            if not testing:
                add_test_case_list = prompt_user_add_update(add_test_case_list, "add")

            add_test_case_list, name_dict = add_new_test_cases(add_test_case_list, jama_client, interpreter)

            add_test_case_list = pull_project_tracking(add_test_case_list, jama_client)

            sync_push_updates(add_test_case_list, jama_client)

            # Go through the list of paths to test files that were first searched and
            # pass them in to see if they need to be updated (if there are any new test cases)
            # We need to pass in the paths to the test files because the test cases themselves
            # have the folder structure paths but not the paths to the test files themselves (Github side)
            # which is what FileInput needs to find the correct test file
            if test_files:
                for test_file in test_files:
                    interpreter.add_gid_file(name_dict, test_file)
            else:
                interpreter.add_gid_file(name_dict, args.test_file)

            if name_dict:
                print("THE FOLLOWING TEST CASES WERE NOT FOUND OR UPDATED IN THE TEST FILE(S):")
                for test_path, test_case_list in name_dict.items():
                    print("\n" + test_path)
                    for key, value in test_case_list.items():
                        print("    " + key + "  : " + value)
                add_status = -1
            else:
                print("If you chose to update, new global IDs were successfully writen to test "
                      "files\nPLEASE REMEMBER TO PUSH NEW GIDS TO GITHUB")
        except Exception as e:
            print("\nFailed to add: " + str(e) + "\n")
    elif args.add:
        print("No test cases were read for ADDING to JAMA")

    # If the user chooses to update, pull the project tracking,
    # prompt the user for the test cases that they will be updating,
    # then sync push the updates
    if args.update and update_test_case_list:
        try:
            update_test_case_list = pull_project_tracking(update_test_case_list, jama_client)

            if not testing:
                update_test_case_list = prompt_user_add_update(update_test_case_list, "update")

            update_status = sync_push_updates(update_test_case_list, jama_client)
        except Exception as e:
            print("\nFailed to update: " + str(e) + "\n")
    elif args.update:
        print("No test cases were read for UPDATING to JAMA")

    # Should be returning 0 if everything executed correctly
    return add_status + update_status


if __name__ == "__main__":
    update_jama(parse_args(sys.argv[1:]))
