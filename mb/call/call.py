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
import os


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
        self.token = os.environ.get("API_TOKEN")
        self.error = None

        # Init object variables
        self.status_code = 0
        self.response = {}

    def get_url(self, endpoint: str):
        """Get a endpoint.

        Args:
            endpoint: the api path
        """
        url = self.url + endpoint

        headers = {"Accept": "application/json", "X-Session-Token": f"{self.token}"}

        try:
            curl_get = requests.get(url, headers=headers)
            self.status_code = curl_get.status_code

            if self.status_code != 200:
                self.response = {}
            else:
                self.response = curl_get.json()
        except Exception as curl_error:
            self.error = str(curl_error)
            self.response = {}
            self.status_code = 0
