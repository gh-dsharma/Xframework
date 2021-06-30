from http import HTTPStatus

import libraries.helper.request_helper

headers = {
    "Content-type": "application/json; charset=UTF-8"
}


def test_request_helper_get():
    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.get("https://reqres.in/api/users")
    assert response.status_code == HTTPStatus.OK


def test_request_helper_post():
    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.post("https://reqres.in/api/users", headers=headers, json={
        "email": "deepika@gmail.com",
        "first_name": "deepika",
        "last_name": "sharma",

    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["email"] == "deepika@gmail.com"
    assert response.json()["first_name"] == "deepika"
    assert response.json()["last_name"] == "sharma"
    assert response.json()["id"]


def test_request_helper_put():
    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.put("https://reqres.in/api/users/2", headers=headers, json={
        "id": 1,
        "email": "deepikassss@gmail.com",
        "first_name": "deepikasss",
        "last_name": "sharma123",
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == "deepikassss@gmail.com"
    assert response.json()["first_name"] == "deepikasss"
    assert response.json()["last_name"] == "sharma123"
    assert response.json()["id"] == 1
