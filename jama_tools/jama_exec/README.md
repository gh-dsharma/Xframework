# Jama Exec
Python script used to update a Jama test plan with local pytest or robot test output xUnit/junit xml files

# Description
This is the beta release of Jama Exec version 1.0.0 

For information behind the planning of this tool, visit the following page:
https://guardanthealth.atlassian.net/wiki/spaces/~312931496/pages/1344899240/Jama+Exec

## Capabilities
- User can update a test plan with 

## Assumptions
- The user has created a test plan AND a test cycle
- The user has filled out the config.json file properly before executing the tool
- The test cycle contains a test version and release candidate 
- The test plan contains a report ID
- The user has created a [Jama API](https://guardanthealth.atlassian.net/wiki/spaces/BSQT/pages/1090033920/How+to+create+a+Jama+API+username+and+password) username and password
- The user holds themselves responsible to review the test plan execution results that the tool has pushed
- The user is using the script responsibly 

## Config file parameters
- "jama_url" - The url for Jama API Access
- "jama_project" - The EXACT Jama project name (Example: "Guardant Software Platform")
- "jama_test_plan" - The EXACT name of the Jama test plan (Example: "TST-123456 ProjectZ v1.0.0")
- "report_id" - The EXACT report ID that will be filled out with this test plan's results 
- "jama_test_cycle" - The EXACT test cycle name (Example: "ProjectZ v1.0.0-RC4")
- "test_version_and_release_candidate" - The EXACT test version with the release candidate (Example: "v1.0.0-RC4")
- "path_to_test_results" - Results xml file path (Example: "libraries/jama_exec/jama_exec_test_cases/robot_output.xml")
- "test_results_type" - Type of the test results output xUnit/junit xml files (currently accepts "robot" or "pytest")
- "bulk_comment" - Any comments that the user would like to leave in each test case results 
(Example: "This test case was tested by Emmit on 09/17/2020")

## Usage
```
./jama_exec.py -h
usage: jama_exec.py [-h] jama_api_username jama_api_password

update Jama test cases based upon a provided pytest file path

positional arguments:
  jama_api_username  password (client ID) for current jama api user
  jama_api_password  password (client secret) for current jama api user

optional arguments:
  -h, --help         show this help message and exit
```

Usage Example:
```
./jama_exec.py z78rxrmi2pgkx0n dw1tbjao5gfext9xkh9xdw3ec
```
