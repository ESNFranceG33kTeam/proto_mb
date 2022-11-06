"""
#############################################
#
# call.py
#
# object for api call
#
#############################################
"""
import requests


class Call:
    """Call class.
    Everything about api call object.
    """

    def __init__(self):
        """Init Call object."""
        self.prefix = "http://"
        self.dns = "127.0.0.1"
        self.port = "8080"
        self.url = self.prefix + self.dns + ":" + self.port + "/"
        self.token = "test"
        self.error = None

        # Init object variables
        self.status_code = 0
        self.response = {}

    def req_url(self, endpoint: str, data: {} = None, protocol: str = "get"):
        """Post a endpoint.

        Args:
            endpoint: the api path
            data: json dict
            protocol: protocol to use can be `get`, `post`, `put` or `delete`
        """
        url = self.url + endpoint

        headers = {"Accept": "application/json", "X-Session-Token": f"{self.token}"}

        try:
            if protocol == "post":
                curl_req = requests.post(url, headers=headers, json=data)
            elif protocol == "put":
                curl_req = requests.put(url, headers=headers, json=data)
            else:
                curl_req = requests.get(url, headers=headers)
            self.status_code = curl_req.status_code

            if self.status_code != 200:
                self.response = {}
            else:
                self.response = curl_req.json()
        except Exception as curl_error:
            self.error = str(curl_error)
            self.response = {}
            self.status_code = 0
