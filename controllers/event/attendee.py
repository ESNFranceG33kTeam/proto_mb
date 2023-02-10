"""
#############################################
#
# attendee.py
#
# object for attendee call
#
#############################################
"""
import pandas as pd
import streamlit as st
from system import Call
from controllers.adherent import Adherent
from controllers.money import Money
from helpers import Configuration, Endpoint
from .event import Event


class Attendee:
    """Attendee class.
    Everything about attendee object.
    """

    def __init__(self):
        """Init Attendee object."""
        self.endpoint = Endpoint.EVE_ATTS
        self.json_pd = None
        self.label = "event-attendee"
        self.req_code = 0
        self.get_data()

        # Legacy
        self.adh_data = Adherent()
        self.eve_data = Event()

        if self.eve_data.json_pd is not None:
            self.eve_data.json_pd = self.eve_data.json_pd.loc[
                (
                    pd.to_datetime(self.eve_data.json_pd["date"])
                    >= (pd.to_datetime("today") - pd.Timedelta("1 days"))
                )
            ]

        # Put/Post
        self.id = 0
        self.id_eve = 0
        self.id_adh = 0
        self.price = 0

    def get_data(self) -> True:
        """Get attendee data."""
        get_req = Call()
        to_return = get_req.get_data(self)
        self.req_code = get_req.status_code
        self.json_pd = get_req.response
        return to_return

    def post_put_data(self, protocol: str):
        """Post or put attendee data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_req = Call()
        payload = {
            "id_event": self.id_eve,
            "id_adherent": self.id_adh,
        }
        post_put_req.post_put_data(obj=self, payload=payload, protocol=protocol)

    def del_data(self):
        """Delete attendee data."""
        del_att = Call()
        del_att.del_data(self)

    def list_attendees(self):
        """List adherents from events aka attendees."""
        st.write("## List of Attendees !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", True)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            feve_filter = f_col.checkbox("Event", False)
            fadh_filter = l_col.checkbox("Adherent", False, disabled=True)

            selected_eve = st.selectbox(
                "Select event name :",
                self.eve_data.json_pd["name"],
                disabled=not feve_filter,
            )
            selected_adh = st.selectbox(
                "Select adherent firstname :",
                self.adh_data.json_pd["firstname"],
                disabled=not fadh_filter,
            )

            s_feve = selected_eve if feve_filter else ""
            s_fadh = selected_adh if fadh_filter else ""

            if feve_filter:
                selected_rows_eve = self.eve_data.json_pd.loc[
                    (self.eve_data.json_pd["name"] == s_feve)
                    & self.eve_data.json_pd["actif"]
                ]
                selected_rows_att = self.json_pd.loc[
                    self.json_pd["id_event"] == selected_rows_eve.index[0]
                ]
                selected_rows_adh = self.adh_data.json_pd.loc[
                    self.adh_data.json_pd.index[
                        selected_rows_att["id_adherent"].tolist()
                    ]
                    - 1
                ]
            elif fadh_filter:
                selected_rows_adh = self.adh_data.json_pd.loc[
                    self.adh_data.json_pd["firstname"] == s_fadh
                ]
                selected_rows_att = self.json_pd.loc[
                    self.json_pd["id_adherent"] == selected_rows_adh.index[0]
                ]
                selected_rows_eve = self.eve_data.json_pd.loc[
                    self.eve_data.json_pd.index[selected_rows_att["id_event"].tolist()]
                    - 1
                ]
            else:
                selected_rows_eve = self.eve_data.json_pd
                selected_rows_adh = self.adh_data.json_pd

            data_eve = selected_rows_eve
            data_adh = selected_rows_adh
        else:
            data_eve = self.eve_data.json_pd
            data_adh = self.adh_data.json_pd

        col_eve, col_adh = st.columns(2)
        with col_eve:
            st.write("### Events")
            st.write(data_eve)

        with col_adh:
            st.write("### Adherents")
            st.write(data_adh)

    def new_attendee(self):
        """Create new attendee."""
        st.write("## Create a new Attendee")

        if self.eve_data.json_pd is None:
            st.warning("Data is empty !")
            return

        selected_indices = st.selectbox(
            "Select row event :", self.eve_data.json_pd.index
        )
        nb_spots_left = (
            self.eve_data.json_pd.loc[selected_indices, "nb_spots_max"]
            - self.eve_data.json_pd.loc[selected_indices, "nb_spots_taken"]
        )
        if nb_spots_left <= 0:
            st.warning("No spot left !")
        else:
            st.success(f"{nb_spots_left} spots left.")
            with st.form("New attendee", clear_on_submit=True):
                self.id_eve = selected_indices
                _ = st.text_input(
                    "Event",
                    self.eve_data.json_pd.loc[selected_indices, "name"],
                    disabled=True,
                )
                self.id_adh = st.number_input("id adherent", min_value=0)
                self.price = st.number_input(
                    "Price",
                    value=self.eve_data.json_pd.loc[selected_indices, "price"],
                    min_value=0,
                )
                payment_type = st.selectbox("Payment type", Configuration().money_type)

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if self.id_eve != 0 and self.id_adh != 0:
                        row_att = self.json_pd.loc[
                            (self.json_pd["id_event"] == self.id_eve)
                            & (self.json_pd["id_adherent"] == self.id_adh)
                        ]
                        if len(row_att.index) != 0:
                            st.warning(
                                f"""
                                `{self.adh_data.json_pd.loc[self.id_adh, 'firstname']}
                                 {self.adh_data.json_pd.loc[self.id_adh, 'lastname']}`
                                 is already an attendee to
                                 `{self.eve_data.json_pd.loc[self.id_eve, 'name']}` event !
                                """
                            )
                        else:
                            # Post attendee
                            self.post_put_data(protocol="post")
                            if self.price > 0:
                                # Post money
                                adh_money = Money()
                                adh_money.label = self.label
                                adh_money.price = self.price
                                adh_money.payment_type = payment_type
                                adh_money.post_data()
                            else:
                                adh_money = Money()
                                adh_money.req_code = 200

                            if self.req_code == 200 and adh_money.req_code == 200:
                                st.success("Attendee and money operation added ✌️")
                            else:
                                error_add_att = (
                                    "Add attendee : " + str(self.req_code)
                                    if self.req_code != 200
                                    else "Add attendee : OK"
                                )
                                error_add_mon = (
                                    "Add money operation : " + str(adh_money.req_code)
                                    if adh_money.req_code != 200
                                    else "Add money operation : OK"
                                )
                                st.error(f"{error_add_att} | {error_add_mon}")
                    else:
                        st.warning(
                            """
                            You forget some info...

                            The `id event`, `id adherent` and `Price` are **MANDATORY**.
                            """
                        )

    def delete_attendee(self):
        """Delete an attendee."""
        st.write("## Delete an Attendee")

        if self.eve_data.json_pd is None:
            st.warning("Data is empty !")
            return

        with st.form("Delete the attendee", clear_on_submit=True):
            self.id_eve = st.number_input("id event", min_value=0)
            self.id_adh = st.number_input("id adherent", min_value=0)

            submitted = st.form_submit_button("Submit")
            if submitted:
                row_att = self.json_pd.loc[
                    (self.json_pd["id_event"] == self.id_eve)
                    & (self.json_pd["id_adherent"] == self.id_adh)
                ]
                if len(row_att.index) == 1:
                    self.id = int(row_att.index[0])
                    self.del_data()
                    if self.req_code == 200:
                        st.success("Attendee deleted ✌️")
                    else:
                        error_del_att = (
                            "Delete attendee : " + str(self.req_code)
                            if self.req_code != 200
                            else "Delete attendee : OK"
                        )
                        st.error(f"{error_del_att}")
                else:
                    st.warning(
                        f"""
                        `{self.adh_data.json_pd.loc[self.id_adh, 'firstname']}
                         {self.adh_data.json_pd.loc[self.id_adh, 'lastname']}`
                         is not an attendee to
                         `{self.eve_data.json_pd.loc[self.id_eve, 'name']}` event !
                        """
                    )

    # def update_attendee(self):
    #    pass
