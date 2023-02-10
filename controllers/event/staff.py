"""
#############################################
#
# staff.py
#
# object for staff call
#
#############################################
"""
import pandas as pd
import streamlit as st
from system import Call
from controllers.volunteer import Volunteer
from controllers.money import Money
from helpers import Configuration, Endpoint
from .event import Event


class Staff:
    """Staff class.
    Everything about staff object.
    """

    def __init__(self):
        """Init Staff object."""
        self.endpoint = Endpoint.EVE_STAS
        self.json_pd = None
        self.label = "event-staff"
        self.req_code = 0
        self.get_data()

        # Legacy
        self.vol_data = Volunteer()
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
        self.id_vol = 0
        self.price = 0

    def get_data(self) -> True:
        """Get staff data."""
        get_req = Call()
        to_return = get_req.get_data(self)
        self.req_code = get_req.status_code
        self.json_pd = get_req.response
        return to_return

    def post_put_data(self, protocol: str):
        """Post or put staff data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_req = Call()
        payload = {
            "id_event": self.id_eve,
            "id_volunteer": self.id_vol,
        }
        post_put_req.post_put_data(obj=self, payload=payload, protocol=protocol)
        self.req_code = post_put_req.status_code

    def del_data(self):
        """Delete staff data."""
        del_req = Call()
        del_req.del_data(self)
        self.req_code = del_req.status_code

    def list_staffs(self):
        """List volunteers from events aka staffs."""
        st.write("## List of Staffs !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", True)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            feve_filter = f_col.checkbox("Event", False)
            fvol_filter = l_col.checkbox("Volunteer", False, disabled=True)

            selected_eve = st.selectbox(
                "Select event name :",
                self.eve_data.json_pd["name"],
                disabled=not feve_filter,
            )
            selected_vol = st.selectbox(
                "Select volunteer firstname :",
                self.vol_data.json_pd["firstname"],
                disabled=not fvol_filter,
            )

            s_feve = selected_eve if feve_filter else ""
            s_fvol = selected_vol if fvol_filter else ""

            if feve_filter:
                selected_rows_eve = self.eve_data.json_pd.loc[
                    (self.eve_data.json_pd["name"] == s_feve)
                    & self.eve_data.json_pd["actif"]
                ]
                selected_rows_sta = self.json_pd.loc[
                    self.json_pd["id_event"] == selected_rows_eve.index[0]
                ]
                selected_rows_vol = self.vol_data.json_pd.loc[
                    self.vol_data.json_pd.index[
                        selected_rows_sta["id_volunteer"].tolist()
                    ]
                    - 1
                ]

            elif fvol_filter:
                selected_rows_vol = self.vol_data.json_pd.loc[
                    self.vol_data.json_pd["firstname"] == s_fvol
                ]
                selected_rows_sta = self.json_pd.loc[
                    self.json_pd["id_volunteer"] == selected_rows_vol.index[0]
                ]
                selected_rows_eve = self.eve_data.json_pd.loc[
                    self.eve_data.json_pd.index[selected_rows_sta["id_event"].tolist()]
                    - 1
                ]
            else:
                selected_rows_eve = self.eve_data.json_pd
                selected_rows_vol = self.vol_data.json_pd

            data_eve = selected_rows_eve
            data_vol = selected_rows_vol
        else:
            data_eve = self.eve_data.json_pd
            data_vol = self.vol_data.json_pd

        col_eve, col_vol = st.columns(2)
        with col_eve:
            st.write("### Events")
            st.write(data_eve)

        with col_vol:
            st.write("### Volunteers")
            st.write(data_vol)

    def new_staff(self):
        """Create new staff."""
        st.write("## Create a new Staff")

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
            with st.form("New staff", clear_on_submit=True):
                self.id_eve = selected_indices
                _ = st.text_input(
                    "Event",
                    self.eve_data.json_pd.loc[selected_indices, "name"],
                    disabled=True,
                )
                self.id_vol = st.number_input("id volunteer", min_value=0)
                self.price = st.number_input(
                    "Price",
                    value=self.eve_data.json_pd.loc[selected_indices, "price"],
                    min_value=0,
                )
                payment_type = st.selectbox("Payment type", Configuration().money_type)

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if self.id_eve != 0 and self.id_vol != 0:
                        row_sta = self.json_pd.loc[
                            (self.json_pd["id_event"] == self.id_eve)
                            & (self.json_pd["id_volunteer"] == self.id_vol)
                        ]
                        if len(row_sta.index) != 0:
                            st.warning(
                                f"""
                                `{self.vol_data.json_pd.loc[self.id_vol, 'firstname']}
                                 {self.vol_data.json_pd.loc[self.id_vol, 'lastname']}`
                                 is already an staff to
                                 `{self.eve_data.json_pd.loc[self.id_eve, 'name']}` event !
                                """
                            )
                        else:
                            # Post staff
                            self.post_put_data(protocol="post")
                            if self.price > 0:
                                # Post money
                                vol_money = Money()
                                vol_money.label = self.label
                                vol_money.price = self.price
                                vol_money.payment_type = payment_type
                                vol_money.post_data()
                            else:
                                vol_money = Money()
                                vol_money.req_code = 200

                            if self.req_code == 200 and vol_money.req_code == 200:
                                st.success("Staff and money operation added ✌️")
                            else:
                                error_add_sta = (
                                    "Add staff : " + str(self.req_code)
                                    if self.req_code != 200
                                    else "Add staff : OK"
                                )
                                error_add_mon = (
                                    "Add money operation : " + str(vol_money.req_code)
                                    if vol_money.req_code != 200
                                    else "Add money operation : OK"
                                )
                                st.error(f"{error_add_sta} | {error_add_mon}")
                    else:
                        st.warning(
                            """
                            You forget some info...

                            The `id event`, `id volunteer` and `Price` are **MANDATORY**.
                            """
                        )

    def delete_staff(self):
        """Delete an staff."""
        st.write("## Delete an Staff")

        if self.eve_data.json_pd is None:
            st.warning("Data is empty !")
            return

        with st.form("Delete the staff", clear_on_submit=True):
            self.id_eve = st.number_input("id event", min_value=0)
            self.id_vol = st.number_input("id volunteer", min_value=0)

            submitted = st.form_submit_button("Submit")
            if submitted:
                row_sta = self.json_pd.loc[
                    (self.json_pd["id_event"] == self.id_eve)
                    & (self.json_pd["id_volunteer"] == self.id_vol)
                ]
                if len(row_sta.index) == 1:
                    self.id = int(row_sta.index[0])
                    self.del_data()
                    if self.req_code == 200:
                        st.success("Staff deleted ✌️")
                    else:
                        error_del_sta = (
                            "Delete staff : " + str(self.req_code)
                            if self.req_code != 200
                            else "Delete staff : OK"
                        )
                        st.error(f"{error_del_sta}")
                else:
                    st.warning(
                        f"""
                        `{self.vol_data.json_pd.loc[self.id_vol, 'firstname']}
                         {self.vol_data.json_pd.loc[self.id_vol, 'lastname']}`
                         is not a staff to
                         `{self.eve_data.json_pd.loc[self.id_eve, 'name']}` event !
                        """
                    )

    # def update_staff(self):
    #    pass
