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

    def __init__(self):
        """Init Money object."""
        self.endpoint = "auth/moneys"
        self.json_pd = None
        self.req_code = 0

        # Post money
        self.label = ""
        self.price = 0

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

    def list_moneys(self):
        """List moneys."""
        st.write("## List of Money operations !")

        s_filter = st.checkbox("Search filters", False)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            label_filter = f_col.checkbox("Label", True)

            selected_label = st.selectbox(
                "Select label :",
                self.json_pd["label"],
                disabled=not label_filter,
            )

            s_label = selected_label if label_filter else ""

            if label_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["label"] == s_label)]
            else:
                selected_rows = self.json_pd

            data_mon = selected_rows
        else:
            data_mon = self.json_pd

        st.write(data_mon.style.format({'price': '{:.2f}'}))

    def new_money(self):
        """Create a new money."""
        st.write("## Create a new Money operation")

        with st.form("New money operation", clear_on_submit=True):
            self.label = st.text_input("Label")
            self.price = st.number_input("Price")

            submitted = st.form_submit_button("Submit")
            if submitted:
                if len(self.label) > 0 and self.price is not None:
                    # Post money
                    self.post_data()

                    if self.req_code == 200:
                        st.success("Money operation added ✌️")
                    else:
                        error_add_mon = (
                            "Add money operation : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add money operation : OK"
                        )
                        st.error(f"{error_add_mon}")
                else:
                    st.warning(
                        """
                        You forget some info...

                        The `label` and `price` are **MANDATORY**.
                        """
                    )
