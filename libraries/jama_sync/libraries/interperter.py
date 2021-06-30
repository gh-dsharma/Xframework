import fileinput
import glob

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List


class Interpreter(ABC):
    @property
    def name(self) -> str:
        return self._name

    @property
    def test_case_indicator(self) -> str:
        return self._test_case_indicator

    @property
    def add_test_case_start_string(self) -> str:
        return self._add_test_case_start_string

    @property
    def update_test_case_start_string(self) -> str:
        return self._update_test_case_start_string

    def get_test_files(self) -> List[str]:
        """
        Return a list of test files if the path is a directory

        Returns:
            A list of test files if the path is a directory
        """
        if Path(self._test_file).is_dir():
            return glob.glob(f"{self._test_file}/**/*.{self._file_extension}", recursive=True)
        else:
            return []

    @abstractmethod
    def filter_test_case_file(self, file_path: str) -> str:
        """
        Read a source file and filter/interpret the data as appropriate for a test case section

        Args:
            file_path: A string representing the path to the source file

        Returns:
            A string representing the testcase section that has been filtered and
            interpreted according to expectations
        """
        pass

    @abstractmethod
    def add_gid_file(self, new_test_case_dict: Dict, file_path: str) -> None:
        """
        Add the global IDs in the dictionary to the <NEW> tags in the source file provided

        Args:
            new_test_case_dict: A dictionary containing old and new test case names (including the GID)
            file_path: A string representing the path to the source file that needs to be updated

        Returns:
            None
        """
        pass


class PytestInterpreter(Interpreter):
    def __init__(self, test_file: str) -> None:
        self._name = 'xframework'
        self._file_extension = 'py'
        self._test_case_indicator = 'def '
        self._add_test_case_start_string = 'def test_NEW_'
        self._update_test_case_start_string = 'def test_gid_'
        self._test_file = test_file

    def filter_test_case_file(self, file_path: str) -> str:
        """
        Read a pytest file and filter/interpret the data as appropriate for a test case section

        Args:
            file_path: A string representing the path to the pytest file

        Returns:
            A string representing the testcase section that has been filtered and
            interpreted according to expectations
        """
        test_case_section = ""

        with open(file_path, 'r') as fp:
            line = fp.readline()
            while line:
                line = fp.readline()

                # If a line has ends with a "\" that indicates that the line is continued
                # on the next. If there are subsequent new lines, keep adding them onto the first line
                if line.strip().endswith("\\"):
                    new_line = ""
                    while line.strip().endswith("\\"):
                        new_line = "\n" + line[:-1].replace("\\", "").strip()

                        # We want to strip the line first then add a space to handle both cases
                        # of a user putting a space after the "\" char and the case where a user
                        # doesn't put a space after the "\"
                        new_line += " "

                        new_line += fp.readline().replace("\n", "").strip()
                        line = new_line
                    test_case_section += new_line
                else:
                    test_case_section += "\n" + line.strip()

        return test_case_section

    def add_gid_file(self, new_test_case_dict: Dict, file_path: str) -> None:
        """
        Add the global IDs in the dictionary to the <NEW> tags in the pytest file provided

        Args:
            new_test_case_dict: A dictionary containing old and new test case names (including the GID)
            file_path: A string representing the path to the pytest file that needs to be updated

        Returns:
            None
        """
        this_file_dict = None

        # Search through the test case dictionary to see if
        # any of the paths match with the pytest file
        for path in new_test_case_dict:

            if path in file_path:
                this_path = path
                this_file_dict = new_test_case_dict[path]

        # If the path is not in the directory, that means
        # the test case does not need to be updated so return
        if not this_file_dict:
            return

        # Iterate through the pytest file and replace the test case name if it was found in the dictionary
        for line in fileinput.input(files=file_path, inplace=1):
            line_stripped = \
                line[line.find(self._test_case_indicator) + len(self._test_case_indicator):line.rfind("(")].strip()

            if line_stripped in this_file_dict:
                line = line.replace(line_stripped, this_file_dict[line_stripped])
                del this_file_dict[line_stripped]

            print(line, end='')

        if not this_file_dict:
            del new_test_case_dict[this_path]


class RobotInterpreter(Interpreter):
    def __init__(self, test_file: str) -> None:
        self._name = 'robot'
        self._file_extension = 'robot'
        self._test_case_indicator = '*** Test Cases ***'
        self._add_test_case_start_string = '<NEW>'
        self._update_test_case_start_string = 'TC-GID'
        self._test_file = test_file

    def filter_test_case_file(self, file_path: str) -> str:
        """
        Filters out all robot file information that is not the
        test case section and returns the test case section as a string

        Args:
            file_path: Path to a robot file

        Returns:
            A string containing the test case section
        """
        test_case_section = False
        test_cases_info = ""

        # Exception for the case where there are too many test case sections
        data = open(file_path, 'r').read()
        test_case_section_count = data.count(self._test_case_indicator)
        if test_case_section_count > 1:
            raise Exception("There are too many test case sections in this file "
                            "(make sure there are no commented out sections "
                            "that contain the string '*** Test Cases ***'")

        with open(file_path, 'r') as fp:
            line = fp.readline()
            while line:
                line = fp.readline()

                # break the loop if we reach the end of the test cases section
                if test_case_section and line.startswith("***"):
                    break

                # read the line if we are in the test cases section
                if line and test_case_section:

                    # If a line has ends with a "\" that indicates that the line is continued
                    # on the next. If there are subsequent new lines, keep adding them onto the first line
                    if line.strip().endswith("\\"):
                        new_line = ""
                        while line.strip().endswith("\\"):
                            new_line = "\n" + line[:-1].replace("...", "").replace("\\", "").strip()

                            # We want to strip the line first then add a space to handle both cases
                            # of a user putting a space after the "\" char and the case where a user
                            # doesn't put a space after the "\"
                            new_line += " "

                            new_line += fp.readline().replace("...", "").replace("\n", "").strip()
                            line = new_line
                        test_cases_info += new_line
                    else:
                        test_cases_info += "\n" + line.replace("...", "").strip()

                # if we reach the indicator, trigger the boolean and start reading
                if self._test_case_indicator == line.strip():
                    test_case_section = True

        return test_cases_info

    def add_gid_file(self, new_test_case_dict: Dict, file_path: str) -> None:
        """
        Add the global IDs in the dictionary to the <NEW> tags in the robot file provided

        Args:
            new_test_case_dict: A dictionary containing old and new test case names (including the GID)
            file_path: A string representing the path to the robot file that needs to be updated

        Returns:
            None
        """

        this_file_dict = None

        # Search through the test case dictionary to see if
        # any of the paths match with the robot file
        for path in new_test_case_dict:
            if path in file_path:
                this_path = path
                this_file_dict = new_test_case_dict[path]

        # If the path is not in the directory, that means
        # the test case does not need to be updated so return
        if not this_file_dict:
            return

        # Iterate through the robot file and replace the test case name if it was found in the dictionary
        for line in fileinput.input(files=file_path, inplace=1):
            line_stripped = line.strip()

            if line_stripped in this_file_dict:
                line = line.replace(line_stripped, this_file_dict[line_stripped])
                del this_file_dict[line_stripped]

            print(line, end='')

        if not this_file_dict:
            del new_test_case_dict[this_path]


class GherkinInterpreter(Interpreter):
    def __init__(self, test_file: str) -> None:
        self._name = 'gherkin'
        self._file_extension = 'feature'
        self._test_case_indicator = 'Scenario: '
        self._add_test_case_start_string = 'Scenario: test_NEW'
        self._update_test_case_start_string = 'Scenario: test_gid'
        self._test_file = test_file

    def filter_test_case_file(self, file_path: str) -> str:
        """
        Read a gherkin file and filter/interpret the data as appropriate for a test case section

        Args:
            file_path: A string representing the path to the gherkin file

        Returns:
            A string representing the testcase section that has been filtered and
            interpreted according to expectations
        """
        test_case_section = ""

        with open(file_path, 'r') as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                test_case_section += "\n" + line.strip()

        return test_case_section

    def add_gid_file(self, new_test_case_dict: Dict, file_path: str) -> None:
        """
        Add the global IDs in the dictionary to the <NEW> tags in the gherkin file provided

        Args:
            new_test_case_dict: A dictionary containing old and new test case names (including the GID)
            file_path: A string representing the path to the gherkin file that needs to be updated

        Returns:
            None
        """
        this_file_dict = None

        # Search through the test case dictionary to see if
        # any of the paths match with the gherkin file
        for path in new_test_case_dict:
            if path in file_path:
                this_path = path
                this_file_dict = new_test_case_dict[path]

        # If the path is not in the directory, that means
        # the test case does not need to be updated so return
        if not this_file_dict:
            return

        # Iterate through the gherkin file and replace the test case name if it was found in the dictionary
        for line in fileinput.input(files=file_path, inplace=1):
            line_stripped = line[line.find(self._test_case_indicator) + len(self._test_case_indicator):].strip()

            if line_stripped in this_file_dict:
                line = line.replace(line_stripped, this_file_dict[line_stripped])
                del this_file_dict[line_stripped]

            print(line, end='')

        if not this_file_dict:
            del new_test_case_dict[this_path]


class InterpreterFactory:
    interpreter_map = {
        'xframework': PytestInterpreter,
        'robot': RobotInterpreter,
        'gherkin': GherkinInterpreter,
    }

    @classmethod
    def create(cls, interpreter_name: str, test_file: str) -> Interpreter:
        return cls.interpreter_map[interpreter_name](test_file)
