"""
#############################################
#
# attendee.py
#
# object for attendee call
#
#############################################
"""
import json
import pandas as pd
import streamlit as st
from system import Call
from controllers.adherent import Adherent
from controllers.money import Money
from .event import Event


class Attendee:
    """Attendee class.
    Everything about attendee object.
    """

    def __init__(self):
        """Init Attendee object."""
        self.endpoint = "auth/event_attendees"
        self.json_pd = None
        self.label = "event-attendee"
        self.req_code = 0

        # Legacy
        self.adh_data = Adherent()
        self.adh_data.get_data()
        self.eve_data = Event()
        self.eve_data.get_data()

        if self.eve_data.json_pd is not None:
            self.eve_data.json_pd = self.eve_data.json_pd.loc[
                (
                    pd.to_datetime(self.eve_data.json_pd["date"])
                    >= (pd.to_datetime("today") - pd.Timedelta("1 days"))
                )
            ]

        # Put/Post
        self.id_att = 0
        self.id_eve = 0
        self.id_adh = 0
        self.staff = False
        self.price = 0

    def get_data(self):
        """Get attendee data."""
        get_list = Call()

        get_list.req_url(endpoint=self.endpoint, protocol="get")
        self.req_code = get_list.status_code

        if get_list.status_code != 200:
            st.warning(get_list.error)
            return

        if get_list.response is None:
            return

        json_dec = json.dumps(get_list.response)
        self.json_pd = pd.read_json(json_dec)
        self.json_pd.set_index("id", inplace=True)

    def post_put_data(self, protocol: str):
        """Post or put attendee data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_att = Call()

        data = {
            "id_event": self.id_eve,
            "id_adherent": self.id_adh,
            "staff": self.staff,
        }

        if protocol == "put":
            self.endpoint = self.endpoint + "/" + str(self.id_att)

        post_put_att.req_url(endpoint=self.endpoint, data=data, protocol=protocol)
        self.req_code = post_put_att.status_code

        if post_put_att.status_code != 200:
            st.warning(post_put_att.error)

    def del_data(self):
        """Delete attendee data."""
        del_att = Call()

        self.endpoint = self.endpoint + "/" + str(self.id_att)
        del_att.req_url(endpoint=self.endpoint, protocol="delete")
        self.req_code = del_att.status_code

        if del_att.status_code != 200:
            st.warning(del_att.error)

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
            fadh_filter = l_col.checkbox("Adherent", False)

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
                self.id_eve = st.number_input("id event", selected_indices)
                self.id_adh = st.number_input("id adherent", min_value=0)
                self.staff = st.checkbox("Staff ?", False)

                pay = st.checkbox(
                    f"Price : {self.eve_data.json_pd.loc[selected_indices, 'price']}€",
                    bool(self.eve_data.json_pd.loc[selected_indices, "price"] <= 0),
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if self.id_eve != 0 and self.id_adh != 0 and pay:
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
                            # Post money
                            adh_money = Money()
                            adh_money.label = self.label
                            adh_money.price = int(
                                self.eve_data.json_pd.loc[selected_indices, "price"]
                            )
                            adh_money.post_data()
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
                    self.id_att = int(row_att.index[0])
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
