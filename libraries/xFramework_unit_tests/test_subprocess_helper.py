from libraries.helper.subprocess_helper import run


def test_gid_204938_run():
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
    run_response = run("echo '\ntesting\nhello world' | grep hello")
    assert run_response == "hello world"


def test_gid_204939_run_negative():
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
    run_response = run("cd nonexistent_folder")
    assert isinstance(run_response, int) and run_response != 0
