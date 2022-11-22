"""
#############################################
#
# event.py
#
# object for event call
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


class Event:
    """Event class.
    Everything about event object.
    """

    def __init__(self):
        """Init Event object."""
        self.endpoint = "auth/events"
        self.json_pd = None
        self.label = "event"
        self.req_code = 0

        # Put/Post event
        self.id_eve = 0
        self.name_eve = ""
        self.date_eve = date(1970, 1, 1)
        self.location_eve = "Mars"
        self.nb_spots_max_eve = 30
        self.nb_spots_taken_eve = 0
        self.type_eve = ""
        self.price_eve = 0
        self.url_facebook_eve = ""
        self.actif_eve = True

    def get_data(self):
        """Get event data."""
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

    def post_put_data(self, protocol: str):
        """Post or put event data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_eve = Call()

        data = {
            "name": f"{self.name_eve}",
            "date": f"{self.date_eve}",
            "location": f"{self.location_eve}",
            "nb_spots_max": self.nb_spots_max_eve,
            "nb_spots_taken": self.nb_spots_taken_eve,
            "type": f"{self.type_eve}",
            "price": self.price_eve,
            "url_facebook": f"{self.url_facebook_eve}",
            "actif": self.actif_eve,
        }

        if protocol == "put":
            self.endpoint = self.endpoint + "/" + str(self.id_eve)

        post_put_eve.req_url(endpoint=self.endpoint, data=data, protocol=protocol)
        self.req_code = post_put_eve.status_code

        if post_put_eve.status_code != 200:
            st.warning(post_put_eve.error)

    def list_events(self):
        """List events."""
        st.write("## List of Events !")

        s_filter = st.checkbox("Search filters", False)
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            fname_filter = f_col.checkbox("Name", True)
            factif_filter = f_col.checkbox("Actif", True)

            selected_name = st.selectbox(
                "Select name :",
                self.json_pd["name"],
                disabled=not fname_filter,
            )

            s_fname = selected_name if fname_filter else ""

            if fname_filter and factif_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["name"] == s_fname)
                    & (self.json_pd["actif"] == factif_filter)
                ]
            else:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["name"] == s_fname)
                    | (self.json_pd["actif"] == factif_filter)
                ]

            data_eve = selected_rows
        else:
            data_eve = self.json_pd.loc[
                (pd.to_datetime(self.json_pd["date"]) >= pd.to_datetime("today"))
            ]

        st.write(data_eve)

    def update_event(self):
        """Update an event to the api."""
        st.write("## Update an Event")
        st.markdown(
            "If you want to auto complete most of the item, selected the `id` of the event."
        )

        up_adh = st.checkbox("Update an Event ?", False)

        if up_adh:
            selected_indices = st.selectbox("Select rows:", self.json_pd.index)

            with st.form("Update", clear_on_submit=False):
                self.id_eve = st.number_input("id", selected_indices)
                self.name_eve = st.text_input(
                    "Name", self.json_pd.loc[selected_indices, "name"]
                )
                date_format = datetime.strptime(
                    self.json_pd.loc[selected_indices, "date"], "%Y-%m-%d"
                )
                self.date_eve = st.date_input("Date", date_format)
                self.location_eve = st.text_input(
                    "Location", self.json_pd.loc[selected_indices, "location"]
                )
                self.nb_spots_max_eve = st.number_input(
                    "Nb spots max", self.json_pd.loc[selected_indices, "nb_spots_max"]
                )
                self.nb_spots_taken_eve = st.number_input(
                    "Nb spots taken",
                    self.json_pd.loc[selected_indices, "nb_spots_taken"],
                )
                self.type_eve = st.selectbox(
                    "Type",
                    Configuration().event_types,
                    Configuration().event_types.index(
                        self.json_pd.loc[selected_indices, "type"]
                    ),
                )
                self.price_eve = st.number_input(
                    "Price", value=self.json_pd.loc[selected_indices, "price"]
                )
                self.url_facebook_eve = st.text_input(
                    "Facebook link", self.json_pd.loc[selected_indices, "url_facebook"]
                )
                self.actif_eve = st.checkbox(
                    "Actif ?", self.json_pd.loc[selected_indices, "actif"]
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if self.id_eve != 0 and len(self.name_eve) > 0:
                        self.post_put_data(protocol="put")
                        if self.req_code == 200:
                            st.success("Event updated ✌️")
                        else:
                            error_up_eve = (
                                "Update event : " + str(self.req_code)
                                if self.req_code != 200
                                else "Update event : OK"
                            )
                            st.error(f"{error_up_eve}")
                    else:
                        st.warning(
                            """
                            You forget some info...

                            The `firstname`, `lastname`, `terms and conditions` are **MANDATORY**.
                            """
                        )

    def new_event(self):
        """Create a new event."""
        st.write("## Create a new Event")

        with st.form("New event", clear_on_submit=True):
            self.name_eve = st.text_input("Name")
            self.date_eve = st.date_input("Date", min_value=date.today())
            self.location_eve = st.text_input("Location")
            self.nb_spots_max_eve = st.number_input("Nb spots max", min_value=0)
            self.nb_spots_taken_eve = 0
            self.type_eve = st.selectbox("Type", Configuration().event_types)
            self.price_eve = st.number_input("Price")
            self.url_facebook_eve = st.text_input("Facebook link")
            self.actif_eve = st.checkbox("Actif ?")

            submitted = st.form_submit_button("Submit")
            if submitted:
                if len(self.name_eve) > 0 and len(self.location_eve) > 0:
                    # Post event
                    self.post_put_data(protocol="post")

                    if self.req_code == 200:
                        st.success("Event added ✌️")
                    else:
                        error_add_eve = (
                            "Add event : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add event : OK"
                        )
                        st.error(f"{error_add_eve}")
                else:
                    st.warning(
                        """
                        You forget some info...

                        The `name`, `location` are **MANDATORY**.
                        """
                    )
