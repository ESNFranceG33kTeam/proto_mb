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
import json
import requests
import pandas as pd
import streamlit as st
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

    def get_data(self, obj: any) -> True:
        """Get obj data.

        Args:
            obj: Object type of money, adherent, volunteer, ...

        Return:
            True/None
        """
        self.req_url(endpoint=obj.endpoint, protocol="get")
        obj.req_code = self.status_code

        if self.status_code != 200:
            st.warning(self.error)
            return None

        if self.response is None:
            return None

        if isinstance(self.response, list):
            self.response = json.dumps(self.response)
            self.response = pd.read_json(self.response)
            self.response.set_index("id", inplace=True)
        else:
            self.response = json.dumps(self.response)
        return True

    def post_put_data(self, obj: any, payload: {}, protocol: str):
        """Post or put data.

        Args:
            obj: Object type of money, adherent, volunteer, ...
            payload: json format of the payload
            protocol: protocol to use, can be `post` or `put`
        """
        if protocol == "put":
            obj.endpoint = obj.endpoint + "/" + str(obj.id_vlt)

        self.req_url(endpoint=obj.endpoint, data=payload, protocol=protocol)
        obj.req_code = self.status_code

        if self.status_code != 200:
            st.warning(self.error)

    def del_data(self, obj: any):
        """Delete data.

        Args:
            obj: Object type of money, adherent, volunteer, ...

        """
        obj.endpoint = obj.endpoint + "/" + str(obj.id_att)
        self.req_url(endpoint=obj.endpoint, protocol="delete")
        obj.req_code = self.status_code
        if self.status_code != 200:
            st.warning(self.error)

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
            elif protocol == "delete":
                curl_req = requests.delete(url, headers=headers)
            else:
                curl_req = requests.get(url, headers=headers)
            self.status_code = curl_req.status_code

            if self.status_code != 200:
                self.response = {}
            else:
                if protocol == "delete":
                    self.response = {}
                else:
                    self.response = curl_req.json()
        except Exception as curl_error:  # pylint: disable=broad-except
            self.error = str(curl_error)
            self.response = {}
            self.status_code = 0
