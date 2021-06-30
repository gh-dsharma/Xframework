# Jama Sync

Python script used to update Jama with local test files

# Description

This is the release of Jama Sync (Jama Sync v3.0.0).

For information behind the tool such as the planning of this tool, visit the following page: [Confluence link](https://guardanthealth.atlassian.net/wiki/spaces/BSQT/pages/1408568331/Jama+Sync)

NOTE: Sync in Jama has two definitions, and I refer to them both explicitly in the code.
Sync (link) means to link the test case to another test case.
Sync (push) means to push the updates to the synced (link) test case.

## Capabilities

- User can add test cases from a file/directory (exclusive)
- User can update test cases from a file/directory (exclusive)
- User can add and update test cases from a file/directory (inclusive)

## Assumptions

- The user follows all [pytest documentation practices](https://guardanthealth.atlassian.net/wiki/spaces/~312931496/pages/1205643831/pytest+package+styling+documentation+standards) or [robot documentation practices](https://guardanthealth.atlassian.net/wiki/spaces/BSQT/pages/1073381879/General+Styling+Guidelines+for+Test+Suite+Test+Case+Development+in+Robot+Framework)
- Test Cases are deleted/deprecated manually both in Github and in Jama
- The root folder (e.g. BIP V&V Protocol) is present in the master Jama project as well as all applicable Jama projects
    - If the folder is NOT in the applicable projects, the test cases will not be added properly and the user will have 
      to delete the test cases in the Jama projects first and re-add them
- The test cases have at least one Jama Project that is NOT the master Jama project (if the user is testing with robot)
    - If any of the test cases ONLY belong to the master Jama project, the user will make note of this and add the 
      other applicable jama projects later on
- This tool is only ran on a master branch (reduces confusion/conflicts between test cases and branches)
- The user holds themselves responsible to push all updated pytest files with new global IDs to Github
- The user has filled out the config.json file properly before executing the tool
- The user has created an API username and password
- The user will refrain from adding/updating more than 30 test cases at a time (keeps user from making large mistakes)
- There are no new test cases with the same name in the same file (e.g. "<NEW> some case" present twice in one file)
- The character "\\" in the documentation is SOLELY for the purpose of line continuation. When a user wants to continue 
  a line, they will put the "\\" character at the end of the initial line and continue on the next line.

## Config file parameters

- "jama_url" - indicates the URL for Jama REST API Access
- "default_test_case_api_type" - indicates a verification test case
- "default_folder_api_type" - indicates a test verification folder
- "default_api_status" - by default, it should indicate a 'Draft' status
- "default_test_case_status" - should be "NOT_SCHEDULED" since we shouldn't be scheduling the 
                             test case with automation (yet)
- "default_master_project" - indicates the master Jama branch that should have all parent test cases
- "jama_project_list" - indicates the list of acceptable projects that can be accessed through the Jama REST API

## Usage

```
./jama_sync.py -h
usage: jama_sync.py [-h] -root_path ROOT_PATH -test_path TEST_PATH -jama_user
                    JAMA_USER -jama_pass JAMA_PASS -interpreter
                    {xframework,robot,gherkin} [--update] [--add]

update Jama test cases based upon a provided test file path

optional arguments:
  -h, --help            show this help message and exit
  -root_path ROOT_PATH  path to the root folder of all test cases that map to
                        Jama
  -test_path TEST_PATH  path to a test file or directory that contains test
                        files
  -jama_user JAMA_USER  username (client ID) for current Jama REST API user
  -jama_pass JAMA_PASS  password (client secret) for current Jama REST API
                        user
  -interpreter {xframework,robot,gherkin}
                        interpreter used to read test files
  --update              update a test case
  --add                 add a test case
```
Usage Example:
```
./jama_sync.py -root_path "./libraries/xFramework_unit_tests/Sample_jama_TC" -test_path "./libraries/xFramework_unit_tests/Sample_jama_TC/test_Api_Automation.py" -jama_user z78rxrmi2pgkx0n -jama_pass dw1tbjao5gfext9xkh9xdw3ec -interpreter xframework --add 
```

## Testing

Prerequisites:
- The test files in test_data/doc_standards have a corresponding folder in the given project that they belong to
- The test files in robot_jama_sync_test has a corresponding folder in the given project that it belongs to
- The test files in xframework_jama_sync_test has a corresponding folder in the given project that it belongs to
- The test files in gherkin_jama_sync_test has a corresponding folder in the given project that it belongs to
- The tester has a Jama REST API username and password
- The tester has access to the test file(s) corresponding folder(s)

To run robot unit tests:
```
pytest -s test_jama_sync_robot.py --username {username} --password {password}
```

To run xframework unit tests:
```
pytest -s test_jama_sync_xframework.py --username {username} --password {password}
```

To run gherkin unit tests:
```
pytest -s test_jama_sync_gherkin.py --username {username} --password {password}
```
