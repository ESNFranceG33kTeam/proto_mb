"""
#############################################
#
# volunteer.py
#
# object for volunteer call
#
#############################################
"""
import json
from datetime import date
from datetime import datetime
import pandas as pd
import streamlit as st
from system import Call
from helpers import Configuration


class Volunteer:
    """Volunteer class.
    Everything about volunteer object.
    """

    def __init__(self):
        """Init Volunteer object."""
        self.endpoint = "auth/volunteers"
        self.json_pd = None
        self.recom_adhesion_price = 5
        self.label = "volunteer"
        self.req_code = 0

        # Put/Post volunteer
        self.id_vlt = 0
        self.firstname_vlt = ""
        self.lastname_vlt = ""
        self.email_vlt = ""
        self.actif = False
        self.bureau = False

        # Adhesion check
        self.adhesion = False

    def get_data(self):
        """Get volunteer data."""
        get_list = Call()

        get_list.req_url(endpoint=self.endpoint, protocol="get")
        self.req_code = get_list.status_code

        if get_list.status_code != 200:
            st.warning(get_list.error)

        json_dec = json.dumps(get_list.response)
        self.json_pd = pd.read_json(json_dec)
        self.json_pd.set_index("id", inplace=True)

    def post_put_data(self, protocol: str):
        """Post or put volunteer data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_vlt = Call()

        data = {
            "firstname": f"{self.firstname_vlt}",
            "lastname": f"{self.lastname_vlt}",
            "email": f"{self.email_vlt}",
            "actif": self.actif,
            "bureau": self.bureau,
        }

        if protocol == "put":
            self.endpoint = self.endpoint + "/" + str(self.id_vlt)

        post_put_vlt.req_url(endpoint=self.endpoint, data=data, protocol=protocol)
        self.req_code = post_put_vlt.status_code

        if post_put_vlt.status_code != 200:
            st.warning(post_put_vlt.error)

    def list_volunteers(self):
        """List volunteers."""
        st.write("## List of Volunteers !")

        s_filter = st.checkbox("Search filters", False)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            fname_filter = f_col.checkbox("Firstname", True)
            lname_filter = l_col.checkbox("Lastname", False)

            selected_firstname = st.selectbox(
                "Select firstname :",
                self.json_pd["firstname"],
                disabled=not fname_filter,
            )
            selected_lastname = st.selectbox(
                "Select lastname :", self.json_pd["lastname"], disabled=not lname_filter
            )

            s_fname = selected_firstname if fname_filter else ""
            s_lname = selected_lastname if lname_filter else ""

            if fname_filter and lname_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["firstname"] == s_fname)
                    & (self.json_pd["lastname"] == s_lname)
                ]
            elif fname_filter or lname_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["firstname"] == s_fname)
                    | (self.json_pd["lastname"] == s_lname)
                ]
            else:
                selected_rows = self.json_pd

            data_vlt = selected_rows
        else:
            data_vlt = self.json_pd

        st.write(data_vlt)
