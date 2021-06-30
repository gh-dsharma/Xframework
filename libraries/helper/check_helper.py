import logging

from .logging_helper import library_logger

def equal(a,b):
    temp = _CheckHelper("equal")
    temp.equal(a,b)

def not_equal(a,b):
    temp = _CheckHelper("not equal")
    temp.not_equal(a,b)

#Written this way to append Check failures to the log. 
#One module method is one class so when it exits, __del__() is called and immediately appends to log
    #otherwise all failures will be appended at the end, instead of immediately after each check

class _CheckHelper:

    import pytest_check as check
    def __init__(self,name):
        
        self.logger = logging.getLogger(__name__) 
        self.initial_failure_count = len(self.check.check_methods._failures)

    def __del__(self):
        #Work around for allure error reports. Name given so its only called once. 
        #Otherwise every instance deletion calls repeatedly appends to log
        if self.name: 
            current_failure_count = len(self.check.check_methods._failures)
            if current_failure_count > self.initial_failure_count:
                last_failure = self.check.check_methods._failures[-1]
                self.logger.error(str(last_failure))
                self.logger.info("Assertion FAIL")
            else:
                self.logger.info("Assertion PASS")

    @library_logger
    def equal(self, a, b):
        """
        It's like an assert but it can continue on failure. Normal asserts stop on failure. 

        :Usage:
            helper.check_helper.equal(True,False) 
            helper.check_helper.equal(True,True) #Continues here even after failure above
        :Returns:
            None
        """
        self.check.equal(a,b)

    @library_logger
    def not_equal(self, a, b):
        """
        It's like an assert but it can continue on failure. Normal asserts stop on failure. 

        :Usage:
            helper.check_helper.equal(True,False) 
            helper.check_helper.equal(True,True) #Continues here even after failure above
        :Returns:
            None
        """
        self.check.not_equal(a,b)



        

    

