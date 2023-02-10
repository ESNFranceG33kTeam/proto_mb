"""
#############################################
#
# money.py
#
# object for adherent call
#
#############################################
"""
from datetime import date
import streamlit as st
from system import Call
from helpers import Configuration, Endpoint


class Money:
    """Money class.
    Everything about money operation object.
    """

    def __init__(self):
        """Init Money object."""
        self.endpoint = Endpoint.MONS
        self.json_pd = None
        self.req_code = 0
        self.get_data()

        # Post money
        self.label = ""
        self.price = 0
        self.payment_date = date.today()
        self.payment_type = "Cash"

    def get_data(self) -> True:
        """Get money data."""
        get_req = Call()
        to_return = get_req.get_data(self)
        self.json_pd = get_req.response
        self.json_pd.drop(columns=["created_at"], inplace=True)
        return to_return

    def post_data(self):
        """Post a money operation data."""
        post_put_req = Call()
        payload = {
            "label": f"{self.label}",
            "price": self.price,
            "payment_type": f"{self.payment_type}",
            "payment_date": f"{self.payment_date}",
        }
        post_put_req.post_put_data(obj=self, payload=payload, protocol="post")

    def list_moneys(self):
        """List moneys."""
        st.write("## List of Money operations !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", False)
        if s_filter:
            label_filter = st.checkbox("Label", True)

            selected_label = st.selectbox(
                "Select label :",
                self.json_pd["label"],
                disabled=not label_filter,
            )

            s_label = selected_label if label_filter else ""

            if label_filter:
                selected_rows = self.json_pd.loc[(self.json_pd["label"] == s_label)]
            else:
                selected_rows = self.json_pd

            data_mon = selected_rows
        else:
            data_mon = self.json_pd

        st.write(data_mon.style.format({"price": "{:.2f}"}))

    def new_money(self):
        """Create a new money."""
        st.write("## Create a new Money operation")

        with st.form("New money operation", clear_on_submit=True):
            self.label = st.text_input("Label")
            self.price = st.number_input("Price")
            self.payment_type = st.selectbox("Payment type", Configuration().money_type)
            self.payment_date = st.date_input(
                "Payment date", self.payment_date, max_value=date.today()
            )

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
