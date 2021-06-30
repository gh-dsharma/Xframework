import pytest
from libraries.helper.check_helper import _CheckHelper


def test_gid_204895_equal():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    check_helper = _CheckHelper("test_helper")
    check_helper.equal(True, True)


# Expecting this to Fail
@pytest.mark.xfail(strict=True)
def test_gid_204896_equal_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) This unit test results with xFail
            ER: This unit test results with xFail
            Notes: This unit test is expected to result with a failure as pytest_check will \
            allow the test to continue it's logic but result the test case itself in a failure. \
            We cannot do a pytest.raises since the failure will not be raised due to pytest_check logic.

    Projects: BI Internal SW Tools
    """
    check_helper = _CheckHelper("test_helper")
    check_helper.equal(True, False)


def test_gid_204897_not_equal():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    check_helper = _CheckHelper("test_helper")
    check_helper.not_equal(True, False)


# Expecting this to Fail
@pytest.mark.xfail(strict=True)
def test_gid_204898_not_equal_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) This unit test results with xFail
            ER: This unit test results with xFail
            Notes: This unit test is expected to result with a failure as pytest_check will \
            allow the test to continue it's logic but result the test case itself in a failure. \
            We cannot do a pytest.raises since the failure will not be raised due to pytest_check logic.

    Projects: BI Internal SW Tools
    """
    check_helper = _CheckHelper("test_helper")
    check_helper.not_equal(True, True)

