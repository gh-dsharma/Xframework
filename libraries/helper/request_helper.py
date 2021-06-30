import requests
import logging


class RequestHelper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get(self, url, *args, **kwargs):
        """
        Sends a get request to a specified url
        :Usage:
            response = request_helper.get(acs_url + "/api/v1/pipeline_types/", headers=auth_headers)
        :Returns:
            the response data from the get request
        """
        self.logger.info("Sending get request to url: " + url +
                         " with the following arguments: " + str(args) + " " + str(kwargs))
        return requests.get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        """
        Sends a post request to a specified url
        :Usage:
            response = request_helper.post(acs_url + "/api/auth/token/create/", headers=headers, json=data)
        :Returns:
            the response data from the post request
        """
        self.logger.info("Sending post request to url: " + url +
                         " with the following arguments: " + str(args) + " " + str(kwargs))
        return requests.post(url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        """
        Sends a put request to a specified url
        :Usage:
            response = request_helper.put(acs_url + "/api/v1/instrument_jobs/" +
                                          test_instrument_uuid + "/" + transition + "/",
                                          headers=auth_headers, json=data)
        :Returns:
            the response data from the put request
        """
        self.logger.info("Sending put request to url: " + url +
                         " with the following arguments: " + str(args) + " " + str(kwargs))
        return requests.put(url, *args, **kwargs)

    def patch(self, url: object, *args: object, **kwargs: object) -> object:
        """
        Sends a patch request to a specified url
        :Usage:
            response = request_helper.patch("https://jsonplaceholder.typicode.com/posts/1",
                                            headers=headers, json=patch_json)
        :Returns:
            the response data from the patch request
        """
        self.logger.info("Sending patch request to url: " + url +
                         " with the following arguments: " + str(args) + " " + str(kwargs))
        return requests.patch(url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        """
        Sends a delete request to a specified url
        :Usage:
            response = request_helper.delete(acs_url + "/api/v1/instruments/" + test_instrument_uuid + "/",
                                          headers=auth_headers, json=data)
        :Returns:
            the response data from the delete request
        """
        self.logger.info("Sending delete request to url: " + url +
                         " with the following arguments: " + str(args) + " " + str(kwargs))
        return requests.delete(url, *args, **kwargs)

    def check_response_code(self, response, expectation):
        """
        Verifies the response code of a requests object response
        :Usage:
            request_helper.check_response_code(response, HTTPStatus.OK)
        """
        self.logger.info("Checking that the response code: '{}' is equal to the expected response code: '{}'"
                         .format(response.status_code, expectation))
        assert response.status_code == expectation

    def check_response_json(self, response, json_value_list, expectation):
        """
        Verifies a specific value in the json of a requests object response. This requires a
        list as the second parameter which is used to iterate through the json keys
        :Usage:
            request_helper.check_response_json(response, ['qualifiers', 0, 'pipeline_type'], pipeline_uuid)
        """
        json_value = response.json()
        key_list = ""
        for i in json_value_list:
            key_list = key_list + "[" + str(i) + "]"
            json_value = json_value[i]
        self.logger.info("Checking that the response.json()" + key_list +
                         ": '" + str(json_value) + "' is equal to the expected json value: '" + str(expectation) + "'")
        assert json_value == expectation

    def check_response_json_exists(self, response, json_value_list):
        """
        Verifies that a value exists within a specific key in the json of a requests object response
        :Usage:
            request_helper.check_response_json_exists(response, ['auth_token'])
        """
        json_value = response.json()
        key_list = ""
        for i in json_value_list:
            key_list = key_list + "[" + str(i) + "]"
            json_value = json_value[i]
        self.logger.info("Checking that the response.json()" + key_list +
                         " contains a value that is not null: " + str(json_value))
        assert json_value
