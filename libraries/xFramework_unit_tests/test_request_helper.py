import pytest

from http import HTTPStatus

from libraries.helper.request_helper import RequestHelper

headers = {
    "Content-type": "application/json; charset=UTF-8"
}


def test_gid_204922_request_helper_get():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]['title'] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"


def test_gid_204923_request_helper_get_negative():
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
    request_helper = RequestHelper()
    with pytest.raises(Exception):
        request_helper.get("https://nonexistenttesturl")


def test_gid_204924_request_helper_post():
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
    request_helper = RequestHelper()
    response = request_helper.post("https://jsonplaceholder.typicode.com/posts", headers=headers, json={
      "title": "foo",
      "body": "bar",
      "userId": 1
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["title"] == "foo"
    assert response.json()["body"] == "bar"
    assert response.json()["userId"] == 1
    assert response.json()["id"]


def test_gid_204925_request_helper_post_negative():
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
    request_helper = RequestHelper()
    with pytest.raises(Exception):
        request_helper.post("https://nonexistenttesturl", headers=headers)


def test_gid_204926_request_helper_put():
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
    request_helper = RequestHelper()
    response = request_helper.put("https://jsonplaceholder.typicode.com/posts/1", headers=headers, json={
      "id": 1,
      "title": "test_title",
      "body": "test_body",
      "userId": 1
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "test_title"
    assert response.json()["body"] == "test_body"
    assert response.json()["userId"] == 1
    assert response.json()["id"] == 1


def test_gid_204927_request_helper_put_negative():
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
    request_helper = RequestHelper()
    with pytest.raises(Exception):
        request_helper.put("https://nonexistenttesturl", headers=headers)


def test_gid_204928_request_helper_patch():
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
    request_helper = RequestHelper()
    response = request_helper.patch("https://jsonplaceholder.typicode.com/posts/1", headers=headers, json={
      "title": "testing_title"
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "testing_title"
    assert response.json()["userId"] == 1
    assert response.json()["id"] == 1


def test_gid_204929_request_helper_patch_negative():
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
    request_helper = RequestHelper()
    with pytest.raises(Exception):
        request_helper.patch("https://nonexistenttesturl", headers=headers)


def test_gid_204930_request_helper_delete():
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
    request_helper = RequestHelper()
    response = request_helper.delete("https://jsonplaceholder.typicode.com/posts/1", headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_gid_204931_request_helper_delete_negative():
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
    request_helper = RequestHelper()
    with pytest.raises(Exception):
        request_helper.delete("https://nonexistenttesturl", headers=headers)


def test_gid_204932_request_helper_check_response_code():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code == HTTPStatus.OK
    request_helper.check_response_code(response, HTTPStatus.OK)


def test_gid_204933_request_helper_check_response_code_negative():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code != HTTPStatus.UNAUTHORIZED
    with pytest.raises(Exception):
        request_helper.check_response_code(response, HTTPStatus.UNAUTHORIZED)


def test_gid_204934_request_helper_check_response_json():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.json()[0]['title'] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    request_helper.check_response_json(response, [0, 'title'],
                                       "sunt aut facere repellat provident occaecati excepturi optio reprehenderit")


def test_gid_204935_request_helper_check_response_json_negative():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.json()[0]['title'] != "test"
    with pytest.raises(Exception):
        request_helper.check_response_json(response, [0, 'title'], "test")


def test_gid_204936_request_helper_check_response_json_exists():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    assert response.json()[0]['title']
    request_helper.check_response_json_exists(response, [0, 'title'])


def test_gid_204937_request_helper_check_response_json_exists_negative():
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
    request_helper = RequestHelper()
    response = request_helper.get("https://jsonplaceholder.typicode.com/posts")
    with pytest.raises(Exception):
        request_helper.check_response_json_exists(response, [0, 'test'])
