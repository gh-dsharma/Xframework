import re

class Test_case_name_parser():

    def __init__(self, request):
        self.nodeid = request.node.nodeid #nodeid:'tests/emerald/test_cases/test_10_non_breast_cancer_type.py::Test_SNV::test_results_are_empty_and_sample_status_fail[Lung Cancer]'

    @property
    def scenario_name(self): #test_results_are_empty_and_sample_status_fail[Lung Cancer]
        return self.nodeid.split("::")[-1] 

    @property
    def class_name(self): #Test_SNV
        delimeter_count = self.nodeid.count("::")
        class_name_exists = delimeter_count == 2
        if class_name_exists:
            return self.nodeid.split("::")[-2] + "_"
        else:
            return '' 

    @property
    def module_path(self): #tests/emerald/test_cases/test_10_non_breast_cancer_type.py
        return self.nodeid.split("::")[0] 
    
    @property
    def file_name(self):
        file_name = self.module_path.split("/" )[-1] #test_10_non_breast_cancer_type.py
        file_name = file_name.split(".")[0] #test_10_non_breast_cancer_type
        return file_name 

    @property
    def project_name(self): #emerald
        return self.module_path.split("/" )[ 1] 

    def get_test_case_name(self): 
        #this is function + scenario eg. test_results_are_empty_and_sample_status_fail[Lung Cancer]
        scenario_name = self.scenario_name
        scenario_name = re.sub('[^0-9a-zA-Z.]+', '_', scenario_name) #remove non-alphanumeric
        return  self.file_name + "_" + self.class_name + scenario_name

    def get_log_name(self):
        test_case_name = self.get_test_case_name()
        return test_case_name + ".log"