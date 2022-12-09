"""
#############################################
#
# attendee.py
#
# object for attendee call
#
#############################################
"""
import os
import json
from datetime import date, time
from calendar_view.calendar import Calendar
from calendar_view.core.event import Event
from calendar_view.core import data
import pandas as pd
import streamlit as st
from system import Call
from controllers.adherent import Adherent
from .planning import Planning


class Attendee:
    """Attendee class.
    Everything about attendee object.
    """

    def __init__(self):
        """Init Attendee object."""
        self.endpoint = "auth/planning_attendees"
        self.json_pd = None
        self.label = "planning-attendee"
        self.req_code = 0

        # Legacy
        self.adh_data = Adherent()
        self.adh_data.get_data()
        self.pla_data = Planning()
        self.pla_data.get_data()
        self.pla_data.json_pd = self.pla_data.json_pd.loc[
            (
                pd.to_datetime(self.pla_data.json_pd["date_end"])
                >= (pd.to_datetime("today") - pd.Timedelta("1 days"))
            )
        ]

        # Put/Post
        self.id_att = 0
        self.id_pla = 0
        self.id_adh = 0
        self.date = date(1970, 1, 1)
        self.hour_begins = time(0, 0, 0)
        self.hour_end = time(23, 59, 59)

        # Calendar view
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cal_att = "{}/{}/".format(current_dir, "../../resources") + "cal_att.png"

    def get_data(self):
        """Get attendee data."""
        get_list = Call()

        get_list.req_url(endpoint=self.endpoint, protocol="get")
        self.req_code = get_list.status_code

        if get_list.status_code != 200:
            st.warning(get_list.error)

        json_dec = json.dumps(get_list.response)
        self.json_pd = pd.read_json(json_dec)
        self.json_pd.set_index("id", inplace=True)

        self.json_pd["date"] = pd.to_datetime(self.json_pd["date"])
        self.json_pd["date"] = self.json_pd["date"].dt.strftime("%Y-%m-%d")
        self.json_pd["hour_begins"] = pd.to_datetime(self.json_pd["hour_begins"])
        self.json_pd["hour_begins"] = self.json_pd["hour_begins"].dt.strftime("%H:%M")
        self.json_pd["hour_end"] = pd.to_datetime(self.json_pd["hour_end"])
        self.json_pd["hour_end"] = self.json_pd["hour_end"].dt.strftime("%H:%M")

    def post_put_data(self, protocol: str):
        """Post or put attendee data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_att = Call()

        payload = {
            "id_planning": self.id_pla,
            "id_adherent": self.id_adh,
            "date": f"{self.date}",
            "hour_begins": f"{self.hour_begins}",
            "hour_end": f"{self.hour_end}",
        }

        if protocol == "put":
            self.endpoint = self.endpoint + "/" + str(self.id_att)

        post_put_att.req_url(endpoint=self.endpoint, data=payload, protocol=protocol)
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

        s_filter = st.checkbox("Search filters", True)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            feve_filter = f_col.checkbox("Planning", False)
            fadh_filter = l_col.checkbox("Adherent", False)

            selected_eve = st.selectbox(
                "Select planning name :",
                self.pla_data.json_pd["name"],
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
                selected_rows_eve = self.pla_data.json_pd.loc[
                    (self.pla_data.json_pd["name"] == s_feve)
                ]
                selected_rows_att = self.json_pd.loc[
                    self.json_pd["id_planning"] == selected_rows_eve.index[0]
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
                selected_rows_eve = self.pla_data.json_pd.loc[
                    self.pla_data.json_pd.index[
                        selected_rows_att["id_planning"].tolist()
                    ]
                ]
            else:
                selected_rows_eve = self.pla_data.json_pd
                selected_rows_adh = self.adh_data.json_pd

            data_eve = selected_rows_eve
            data_adh = selected_rows_adh
        else:
            data_eve = self.pla_data.json_pd
            data_adh = self.adh_data.json_pd

        col_eve, col_adh = st.columns(2)
        with col_eve:
            st.write("### Plannings")
            st.write(data_eve)

        with col_adh:
            st.write("### Adherents")
            st.write(data_adh)

    def cal_attendees(self):
        """View attendees calendar."""
        st.write("### View attendees calendar")

        def gen_cal(indice: int):
            """Function to gen the calendar.

            Args:
                indice: indice selected for the filter.
            """
            if (
                self.pla_data.json_pd.loc[indice, "date_begins"]
                == self.pla_data.json_pd.loc[indice, "date_end"]
            ):
                time_delta = f"{self.pla_data.json_pd.loc[indice, 'date_begins']}"
            else:
                time_delta = (
                    f"{self.pla_data.json_pd.loc[indice, 'date_begins']} - "
                    f"{self.pla_data.json_pd.loc[indice, 'date_end']}"
                )

            config = data.CalendarConfig(
                lang="en",
                title=f"{self.pla_data.json_pd.loc[indice, 'name']}",
                dates=time_delta,
                show_year=True,
                mode=None,
                legend=False,
            )
            events = []
            for id_adherent, date_att, hour_begins, hour_end in zip(
                self.json_pd["id_adherent"],
                self.json_pd["date"],
                self.json_pd["hour_begins"],
                self.json_pd["hour_end"],
            ):
                firstname_att = self.adh_data.json_pd.loc[id_adherent, "firstname"]
                lastname_att = self.adh_data.json_pd.loc[id_adherent, "lastname"]
                events.append(
                    Event(
                        f"{firstname_att} {lastname_att}",
                        day=date_att,
                        start=hour_begins,
                        end=hour_end,
                    )
                )

            data.validate_config(config)
            data.validate_events(events, config)
            calendar = Calendar.build(config)
            calendar.add_events(events)
            calendar.save(self.cal_att)

        selected_indice = st.selectbox(
            "Select row event :", self.pla_data.json_pd.index
        )
        self.json_pd = self.json_pd.loc[self.json_pd["id_planning"] == selected_indice]

        if st.checkbox("View planning"):
            gen_cal(indice=selected_indice)
            st.image(self.cal_att)

    def new_attendee(self):
        """Create new attendee."""
        st.write("## Create a new Attendee")

        with st.form("New attendee", clear_on_submit=True):
            self.id_pla = st.number_input("id planning", min_value=0)
            self.id_adh = st.number_input("id adherent", min_value=0)
            self.date = st.date_input("date")
            self.hour_begins = st.time_input("Hour begins")
            self.hour_end = st.time_input("Hour end")

            submitted = st.form_submit_button("Submit")
            if submitted:
                if self.id_pla != 0 and self.id_adh != 0:
                    row_att = self.json_pd.loc[
                        (self.json_pd["id_planning"] == self.id_pla)
                        & (self.json_pd["id_adherent"] == self.id_adh)
                    ]
                    if len(row_att.index) != 0:
                        st.warning(
                            f"""
                                `{self.adh_data.json_pd.loc[self.id_adh, 'firstname']}
                                 {self.adh_data.json_pd.loc[self.id_adh, 'lastname']}`
                                 is already an attendee to
                                 `{self.pla_data.json_pd.loc[self.id_pla, 'name']}` planning !
                                """
                        )
                    else:
                        # Post attendee
                        self.post_put_data(protocol="post")

                        if self.req_code == 200:
                            st.success("Attendee added ✌️")
                        else:
                            error_add_att = (
                                "Add attendee : " + str(self.req_code)
                                if self.req_code != 200
                                else "Add attendee : OK"
                            )
                            st.error(f"{error_add_att}")
                else:
                    st.warning(
                        """
                        You forget some info...

                        The `id planning`, `id adherent` are **MANDATORY**.
                        """
                    )

    def delete_attendee(self):
        """Delete an attendee."""
        st.write("## Delete an Attendee")

        with st.form("Delete the attendee", clear_on_submit=True):
            self.id_pla = st.number_input("id planning", min_value=0)
            self.id_adh = st.number_input("id adherent", min_value=0)

            submitted = st.form_submit_button("Submit")
            if submitted:
                row_att = self.json_pd.loc[
                    (self.json_pd["id_planning"] == self.id_pla)
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
                         `{self.pla_data.json_pd.loc[self.id_pla, 'name']}` planning !
                        """
                    )

    # def update_attendee(self):
    #    pass
