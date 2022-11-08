"""
#############################################
#
# call.py
#
# object for api call
#
#############################################
"""
import os
import requests
from helpers import Configuration


class Call:
    """Call class.
    Everything about api call object.
    """

    def __init__(self):
        """Init Call object."""
        myconf = Configuration()

        self.prefix = myconf.api_prefix
        self.dns = myconf.api_dns
        self.port = myconf.api_port
        self.url = self.prefix + self.dns + ":" + self.port + "/"
        self.token = os.environ.get(myconf.api_token)
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
        except Exception as curl_error:  # pylint: disable=broad-except
            self.error = str(curl_error)
            self.response = {}
            self.status_code = 0
