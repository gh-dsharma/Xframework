class TestResult:
    """
    A class to pass information about a test case in jama_sync.py
    """
    def __init__(self, name, runtime, jama_result):
        """
        TestCase initializer. Most information in the test case
        will be filled out after it is initialized

        :name: name or title of the test case (should start with a TC-GID-XXXXX)
        """
        self.name = name
        self.runtime = runtime
        self.jama_result = jama_result
        self.failed_test_case = None
        self.failure_type = None
        self.failure_message = None
        self.jama_result_message = None
        self.jama_global_id = None
        self.jama_test_case_id = None
        self.jama_test_run_id = None

    def set_failed(self, failure_type, failure_message, test_plan, test_version):
        self.failed_test_case = True
        self.failure_type = failure_type
        self.failure_message = failure_message
        self.jama_result_message = "Failed. Tested for test plan '" + test_plan + \
                                   "' on software version '" + test_version + "'. "
        if self.failure_type == "failure":
            self.jama_result_message += "\nTest case failed with the following reason: " + self.failure_message
        elif self.failure_type == "error":
            self.jama_result_message += "\nTest case ran into an error with the following reason: " + \
                                        self.failure_message
        else:
            print(failure_type)
            print(failure_message)
            raise Exception("Ran into an unexpected failure type:", self.failure_type)

    def set_passed(self, test_plan, test_version):
        self.failed_test_case = False
        self.jama_result_message = "Passed. Tested for test plan '" + test_plan + \
                                   "' on software version '" + test_version + "'. "

    def set_bulk_comment(self, assinged_user, comment):
        self.failed_test_case = False
        self.jama_result_message += "\n\nTest case executer '" + assinged_user + \
                                    "' has left the following comment: " + comment

    def set_jama_global_id(self, jama_global_id):
        self.jama_global_id = jama_global_id

    def set_jama_test_case_id(self, jama_test_case_id):
        self.jama_test_case_id = jama_test_case_id

    def set_jama_test_run_id(self, jama_test_run_id):
        self.jama_test_run_id = jama_test_run_id

    def get_name(self):
        return self.name

    def get_runtime(self):
        return self.runtime

    def get_jama_test_case_id(self):
        return self.jama_test_case_id

    def get_jama_test_run_id(self):
        return self.jama_test_run_id

    def get_jama_result(self):
        return self.jama_result

    def get_jama_result_message(self):
        return self.jama_result_message

    def __str__(self):
        """
        Returns string representation for print functions
        """
        string_representation = "*******************************************************************************\n"

        string_representation += "Test case: " + self.name + "\n"
        string_representation += "      Result: " + self.jama_result + "\n"
        if self.failed_test_case:
            string_representation += "          Failure result type: " + self.failure_type + "\n"
        if self.jama_global_id:
            string_representation += "Jama Global ID: " + self.jama_global_id + "\n"
            string_representation += "Jama Global Test Case ID: " + str(self.jama_test_case_id) + "\n"
        string_representation += "\nJama Message: " + self.jama_result_message + "\n"

        string_representation += "*******************************************************************************\n\n\n"

        return string_representation
