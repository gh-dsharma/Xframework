## Description
xFramework Version: 1.0

The repo contains a small project as an example for the pytest framework. Refer to 'preconditions' and 'quick start' to get started. Helpful links below:
Pytest introduction for pytest concepts [conlfuence page](https://guardanthealth.atlassian.net/wiki/spaces/~49147252/pages/1271466436/Pytest+Overview)
Framework feature check list [conlfuence page](https://guardanthealth.atlassian.net/wiki/spaces/BSQT/pages/1313250806/Framework+Checklist)

## Precondition
1. Python 3.7+ installed or setup a [virtual environment](https://guardanthealth.atlassian.net/wiki/spaces/BSQT/pages/923533763/Create+a+new+conda+Environment+in+HPC+dev)

2. Git is installed

3. Install requirements.txt:
```
pip install -r requirements.txt --no-deps
```

## Quick Start

run xframework demo project
```
pytest -m hamster_demo
```
Run for debugging. Args explanation: -s shows print statements, -l shows local values, -tb shows traceback, -m are marks 
```
pytest -s -l --tb=short -m hamster_demo 
```

## Directory Structure
```
.
├── libraries                   <--- common framework functions
│   ├── framework               <--- functions specific to framework
│   ├── helper                  <--- functions secific to libraries  eg. json, os, docker
    │   ├── json_helper
    │   ├── docker_helper       <--- curated functions with logging so you don't have to go through docs
        └── ...   
│   └── unit_tests        
└── tests
    ├── hamster_demo            <--- project specific folder. This is what we use as template for different projects
    │   ├── data
    │   ├── libraries
    │   ├── test_cases
    │   └── logs
    └── api_demo                <--- project specific folder. This is what we use as template for different projects
        └── ...      
├── pytest.ini                  <--- pytest aliases for commandline
├── README.md
├── requirements.txt
├── conftest.py

```

## Libraries 
1. check - to perform multiple assertions in a single test case
2. docker - controls for docker objects
3. pandas - convert tsv/csv bip files to dataframes for data processing
4. json - controls for json files
5. jmespath - traversing json objects similar to xpath 
6. subprocess - used for bash command lines
7. path - used for file paths
8. tavern - API testing
9. request - API testing
10. mock - mocking functionality





