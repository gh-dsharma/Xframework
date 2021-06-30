#!/usr/bin/env python
# content of jama_sync.py

import argparse
import sys
import glob

from jama_api import JamaClientHelper
import io
import os
import fileinput
import json
import traceback
from junitparser import JUnitXml
from test_result import TestResult

curr_dir = os.path.dirname(__file__)
config_path = os.path.join(curr_dir, 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)


def initialize_jama_client(jama_username, jama_password):
    """
    Return an initialized JamaClientHelper

    Args:
        jama_username: Username for the jama client in the constants
        jama_password: Password for the jama client in the constants

    Returns: A string containing the test case section
    """
    return JamaClientHelper(config['jama_url'], jama_username, jama_password)


def parse_args(args):
    """
    Return an ArgumentParser object containing the arguments passed in

    Args:
        args: A list of arguments to be parsed

    Returns: An ArgumentParser object containing the arguments passed in
    """
    parser = argparse.ArgumentParser(description='update Jama test cases based upon a provided pytest file path')
    parser.add_argument("jama_api_username", help="password (client ID) for current jama api user")
    parser.add_argument("jama_api_password", help="password (client secret) for current jama api user")
    return parser.parse_args(args)


def check_report_id_in_test_plan(report_id, jama_test_plan):
    """
    Check that the Report ID is in the Jama Test Plan name

    Args:
        report_id: A string representing a Report ID
        jama_test_plan: A string representing a Jama Test Plan name
    """
    if report_id not in jama_test_plan:
        raise Exception("\nReport id '" + report_id + "' is not listed in the Jama test plan '" +
                        jama_test_plan + "', please add the report id to the Jama test plan and try again")


def check_version_in_test_cycle(test_version, jama_test_cycle):
    """
    Check that the version of the software that was tested is in the Jama Test Cycle name

    Args:
        test_version: A string representing the test version of the software that was tested
        jama_test_cycle: A string representing a Jama Test Cycle name
    """
    if test_version not in jama_test_cycle:
        raise Exception("\nTest version '" + test_version + "' is not listed in the Jama test cycle '" +
                        jama_test_cycle + "', please add the test version and release candidate to " +
                        "the Jama test cycle and try again")


def read_results_from_suites(xml_suite, test_results_list):
    """
    Read the output xml file (formatted to read from a suite) and return a list of Test Result objects

    Args:
        xml_suite: An xml file output formatted as a single xml suite
        test_results_list: A list of test results that test results are getting added to

    Returns: A list of Test Result objects
    """
    for case in xml_suite:
        if case.result:
            if case.result._tag != "skipped":
                new_result = TestResult(case.name, case.time, "FAILED")
                new_result.set_failed(case.result._tag, case.result.message,
                                      config['jama_test_plan'], config['test_version_and_release_candidate'])
                test_results_list.append(new_result)
        else:
            new_result = TestResult(case.name, case.time, "PASSED")
            new_result.set_passed(config['jama_test_plan'], config['test_version_and_release_candidate'])
            test_results_list.append(new_result)
    return test_results_list


def read_output_xml_file(xml_file):
    """
    Read the output xml file and return a list of Test Result objects

    Args:
        xml_file: A string that contains the path to the xml output file that will be read

    Returns: A list of Test Result objects
    """
    xml = JUnitXml.fromfile(xml_file)
    test_results_read = []
    # Typically reading from a pytest output xml when the first tag is "testsuites".
    # We shouldn't be using this ._tag like below as it's protected by the class but there's currently no cleaner way \
    # to get this other than turning the element into a string and looking for expected keywords
    if xml._tag == "testsuites":
        print("---------------------Reading from " + xml_file + "---------------------")
        for suite in xml:
            test_results_read = read_results_from_suites(suite, test_results_read)
        return test_results_read
    # typically reading from a robot output xml with this
    else:
        print("---------------------Reading from " + xml_file + "---------------------")
        return read_results_from_suites(xml, test_results_read)


def get_test_case_jama_ids(jama_client, project, test_results, test_case_type):
    """
    Check that the version of the software that was tested is in the Jama Test Cycle name

    Args:
        jama_client: An initialized jama client object made from the JamaClientHelper
        project: A string representing the Jama project that the test runs live in
        test_results: A list of test result objects
        test_case_type: A string representing the framework that was used to output the xml results (ex: pytest)

    Returns: An array of TestCase objects representing all test case information that was passed in
    """
    valid_test_case_types = ["pytest", "robot"]
    if test_case_type not in valid_test_case_types:
        raise Exception("Jama Exec does not currently support '" + test_case_type +
                        "' types of test case updates currently. Please enter one of the valid test case types:" +
                        str(valid_test_case_types))

    project_id = jama_client.get_project_id(project)

    # Go through the test results and retrieve the global ID (might be needed for later) and test case ID
    # then return the test results with the Jama IDs set
    if test_case_type == "pytest":
        for test_result in test_results:
            if not test_result.name.startswith("test_gid_"):
                raise Exception("Error in test case names. Expecting 'test_gid_' "
                                "in the following pytest test case name:", test_result.name)
            global_id = "GID-" + test_result.name.strip("test_gid_").split("_")[0]
            test_result.set_jama_global_id(global_id)
            test_case_id = jama_client.get_test_case_id_from_global_id(project, project_id, global_id)
            test_result.set_jama_test_case_id(test_case_id)
        return test_results
    elif test_case_type == "robot":
        for test_result in test_results:
            if not test_result.name.startswith("TC-GID-"):
                raise Exception("Error in test case names. Expecting 'TC-GID-' "
                                "in the following robot test case name:", test_result.name)
            global_id = test_result.name.strip("TC-").split(":")[0]
            test_result.set_jama_global_id(global_id)
            test_case_id = jama_client.get_test_case_id_from_global_id(project, project_id, global_id)
            test_result.set_jama_test_case_id(test_case_id)
        return test_results


def notify_user_of_deltas(in_executed_but_not_in_jama_delta, in_jama_but_not_in_executed_delta):
    """
    Prints the delta in command line

    Args:
        in_executed_but_not_in_jama_delta: A list containing test case names that were executed but not in jama
        in_jama_but_not_in_executed_delta: A list containing test case names that are in jama but were not executed
    """
    if in_executed_but_not_in_jama_delta or in_jama_but_not_in_executed_delta:
        print("\n--------------------USER WARNINGS--------------------")
        if in_executed_but_not_in_jama_delta:
            print("The following test cases were executed but NOT in the Jama Test Plan:")
            for test_case in in_executed_but_not_in_jama_delta:
                print("     " + test_case)

        # Spacer
        if in_executed_but_not_in_jama_delta and in_jama_but_not_in_executed_delta:
            print()

        if in_jama_but_not_in_executed_delta:
            print("The following test cases were in the Jama Test Plan but were NOT executed:")
            for test_case in in_jama_but_not_in_executed_delta:
                print("     " + test_case)
        print("--------------------USER WARNINGS--------------------")


def read_output_and_format(jama_client, project, path_to_output, framework_type):
    """
    Read an output xml file and return a list of test result objects containing the result information

    Args:
        jama_client: An initialized jama client object made from the JamaClientHelper
        project: A string representing the Jama project that the test runs live in
        path_to_output: The path to the output xml file
        framework_type: A string representing the framework that was used to output the xml results (ex: pytest)

    Returns: A list of test result objects containing the result information
    """
    # Read an output xml file and get the test results object list
    test_results = read_output_xml_file(path_to_output)

    # Get test case Jama IDs associated with test cases in the test results
    test_results_with_ids = get_test_case_jama_ids(jama_client, project, test_results, framework_type)

    return test_results_with_ids


def update_jama_with_results(jama_client, jama_project, jama_test_plan, report_id,
                             jama_test_cycle, test_version_and_release_candidate, bulk_comment, test_results):
    """
    Updates Jama with the test case results and returns the delta

    Args:
        jama_client: An initialized jama client object made from the JamaClientHelper
        jama_project: A string representing the Jama project that the test runs live in
        jama_test_plan: A string representing the name of the Jama test plan
        report_id: A string representing the report ID that is associated with this test plan
        jama_test_cycle: A string representing the cycle that is being tested
        test_version_and_release_candidate: A string representing the Jama test version and release candidate associated
        bulk_comment: A string representing the comment that the user provided to add to the test runs
        test_results: A list of test result objects
    """
    # Retrieve the jama user ID of the current user (jama API credentials)
    user_jama_id, user_full_name = jama_client.get_current_user_id()

    # Get the project id and test plan
    project_id = jama_client.get_project_id(jama_project)
    test_plan_id = jama_client.get_test_plan_id(project_id, jama_test_plan)

    # Get the test cycle
    test_cycle_id = jama_client.get_test_cycle_id(test_plan_id, jama_test_cycle)

    # # Check that the jama test plan and jama test cycle have the report ID and version with the release candidate
    check_report_id_in_test_plan(report_id, jama_test_plan)
    check_version_in_test_cycle(test_version_and_release_candidate, jama_test_cycle)

    # Get the test runs and the test cases needed to update from Jama
    test_runs = jama_client.get_test_runs(test_cycle_id)

    # Go through the test runs and create two dicts:
    #   jama_test_runs: a dict that maps a test run id to the test run data
    #   jama_test_case_to_test_run_ids: a dict that maps a test case ids to test run ids
    jama_test_runs = {}
    jama_test_case_to_test_run_ids = {}
    for test_run in test_runs:
        jama_test_runs[test_run['id']] = test_run
        jama_test_case_to_test_run_ids[test_run['fields']['testCase']] = test_run['id']

    # Go through the actual executed test results and create two lists:
    #   executed_test_results: a list of test run ids that were actually executed
    #   executed_but_not_in_jama_test_plan: a list of test case names of cases that were executed but are NOT in Jama
    executed_test_results = []
    executed_but_not_in_jama_test_plan = []
    for test_result in test_results:
        if test_result.get_jama_test_case_id() in jama_test_case_to_test_run_ids.keys():
            jama_run_id = jama_test_case_to_test_run_ids[test_result.get_jama_test_case_id()]
            test_result.set_jama_test_run_id(jama_run_id)
            executed_test_results.append(jama_run_id)
        else:
            executed_but_not_in_jama_test_plan.append(test_result.get_name())

    # Go through the difference in test cases that were in Jama but not executed and create a list
    jama_test_plan_but_not_in_executed = []
    for test_run_id in (jama_test_runs.keys() - executed_test_results):
        jama_test_plan_but_not_in_executed.append(jama_test_runs[test_run_id]['fields']['name'])

    # Get the similarities between the list of test cases that were executed vs what is in Jama
    test_results_to_update = executed_test_results & jama_test_runs.keys()

    print()  # Spacer

    # Go through the test results again and push the result to Jama if the test case is in Jama
    for test_result in test_results:
        if test_result.get_jama_test_run_id() in test_results_to_update:
            if bulk_comment:
                test_result.set_bulk_comment(user_full_name, bulk_comment)
            jama_client.update_test_run(jama_test_runs[test_result.get_jama_test_run_id()],
                                        test_result.get_jama_result(),
                                        test_result.get_jama_result_message(),
                                        test_result.get_runtime(), user_jama_id, bulk_comment)

    # return the delta
    return executed_but_not_in_jama_test_plan, jama_test_plan_but_not_in_executed


if __name__ == "__main__":

    # Parse the arguments
    parsed_args = parse_args(sys.argv[1:])

    # Initialize the Jama client to interface with Jama APIs
    this_jama_client = initialize_jama_client(parsed_args.jama_api_username, parsed_args.jama_api_password)

    # Read the results output
    test_result_list = read_output_and_format(this_jama_client, config['jama_project'],
                                              config['path_to_test_results'], config['test_results_type'])

    # Push results to Jama and retrieve the delta
    executed_delta, jama_delta = update_jama_with_results(this_jama_client, config['jama_project'],
                                                          config['jama_test_plan'], config['report_id'],
                                                          config['jama_test_cycle'],
                                                          config['test_version_and_release_candidate'],
                                                          config['bulk_comment'],
                                                          test_result_list)

    # Report the test case delta to user
    notify_user_of_deltas(executed_delta, jama_delta)
