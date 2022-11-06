"""
#############################################
#
# money.py
#
# object for adherent call
#
#############################################
"""
import json
import pandas as pd
import streamlit as st
from call import Call


class Money:
    """Money class.
    Everything about money operation object.
    """

    def __init__(self, label: str, price: int):
        """Init Money object.

        Args:
            label: label of the operation
            price: among of the operation
        """
        self.endpoint = "auth/moneys"
        self.json_pd = None
        self.req_code = 0

        # Post money
        self.label = label
        self.price = price

    def get_data(self):
        """Get money data."""
        get_list = Call()

        get_list.req_url(endpoint=self.endpoint, protocol="get")
        self.req_code = get_list.status_code

        if get_list.status_code != 200:
            st.warning(get_list.error)

        for mon in get_list.response:
            del mon["created_at"]

        json_dec = json.dumps(get_list.response)
        self.json_pd = pd.read_json(json_dec)
        self.json_pd.set_index("id", inplace=True)

    def post_data(self):
        """Post a money operation data."""
        post_mon = Call()

        data = {"label": f"{self.label}", "price": self.price}

        post_mon.req_url(endpoint=self.endpoint, data=data, protocol="post")
        self.req_code = post_mon.status_code

        if post_mon.status_code != 200:
            st.warning(post_mon.error)
