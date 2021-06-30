from http import HTTPStatus

import libraries.helper.request_helper

def test_gid_265849_verify_fetch_user_detail():
    """
        Description:
            Verify the fetch user get request for medical software

        Prerequisites:
            1) User should be available in the oracle database

        Test Data: NA

        Steps:
            1) Run the GET Api for the users available in database
                ER: Users should get fetched
                Notes: check users
            2) Verify the valid record is generated
                ER: All the records should be generated in the database
                Notes: Verify the records from database

        Projects:SANBOX_BI
        """
    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.get("https://reqres.in/api/users")
    assert response.status_code == HTTPStatus.OK


def test_gid_265850_verify_Creating_resource():
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

           Projects:SANBOX_BI
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


def test_gid_265851_verify_update_request():
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

           Projects:SANBOX_BI
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

def test_gid_265852_verify_delete_request():
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

               Projects:SANBOX_BI
               """

    request_helper = libraries.helper.request_helper.RequestHelper()
    response = request_helper.get("https://reqres.in/api/users/2", headers=headers)
    assert response.status_code == HTTPStatus.OK



