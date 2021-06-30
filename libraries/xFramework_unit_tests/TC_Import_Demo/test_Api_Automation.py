from http import HTTPStatus

import libraries.helper.request_helper

headers = {
    "Content-type": "application/json; charset=UTF-8"
}


def test_gid_264665_get():
    """
        Description:
            Verify the fetch user request

        Prerequisites:
            1) User should be available in the database

        Test Data: NA

        Steps:
            1) Run the GET Api for the users available in database
                ER: Users should get fetched
                Notes: check users

        Projects:Screening O2C
        """
    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.get("https://reqres.in/api/users")
    assert response.status_code == HTTPStatus.OK


def test_gid_264666_post():
    """
           Description:
               Verify the Post user request to create Resource

           Prerequisites:
               1) The data should be created

           Test Data: NA

           Steps:
               1) Run the POST Api for creating a new resource
                   ER: The data of users should be created
                   Notes: check users

           Projects:Screening O2C
           """

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


def test_gid_264667_put():
    """
           Description:
               Verify the Put user request

           Prerequisites:
               1) The user data should be updated

           Test Data: NA

           Steps:
               1) Run the PUT Api for the users available in database
                   ER: The data of Users should be updated
                   Notes: check users

           Projects:Screening O2C
           """

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




