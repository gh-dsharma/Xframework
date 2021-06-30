import logging
from pathlib import Path
from .test_case_name_parser import Test_case_name_parser
import re

def testcase_logger(request, logging_level):

    #meta data
    test_case_mapping = Test_case_name_parser(request)

    #create loggers
    logger_for_framework = logging.getLogger() #You can limit the scope by extending to libraries.helper eg. logging.getLogger('libraries.helper') 
    logger_for_framework.setLevel(logging_level)
    logger_for_testcases = logging.getLogger(request.function.__name__)
    logger_for_testcases.setLevel(logging_level)
    
    #create file handler
    logs_folder_file_path = Path(__file__).parent.parent.parent / "tests/" / test_case_mapping.project_name / "logs/TestCaseLogs/"
    logs_folder_file_path = str(logs_folder_file_path.resolve()) + "/"
    file_name = test_case_mapping.get_log_name()
    handler = logging.FileHandler(logs_folder_file_path + file_name, 'w+') 
    handler.setLevel(logging_level)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the file handler to the logger
    logger_for_framework.addHandler(handler)
    yield logger_for_testcases
    handler.close()
    logger_for_framework.removeHandler(handler)