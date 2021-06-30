import pytest


def test_gid_195051_addition():
    sum_of_addition = 1 + 2
    assert sum_of_addition == 3


def test_gid_195052_subtraction():
    difference = 3 - 2
    assert difference == 2


def test_gid_196301_raise_exception():
    raise Exception("testing exception")


def test_gid_196302_errors(nonexistent_parameter):
    assert nonexistent_parameter


def test_gid_123456789_not_a_jama_test_case():
    pass

@pytest.mark.skip(reason="testing skip")
def test_skip():
    raise Exception("testing")
