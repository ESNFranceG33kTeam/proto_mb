"""
#############################################
#
# card.py
#
# object for volunteer card
#
#############################################
"""
import json
import copy
from datetime import datetime
import streamlit as st
from system import Call
from helpers import Endpoint


class Card:
    """Card class.
    Everything about card object.
    """

    def __init__(self):
        """Init Card object."""
        self.label = "card"
        self.json_pd = None
        self.get_req = Call()

        # Legacy
        self.endpoint = Endpoint.ADHS
        self.get_req.get_data(self)
        self.json_pd_adh = copy.copy(self.get_req.response)
        self.endpoint = Endpoint.VLTS
        self.get_req.get_data(self)
        self.json_pd_vlt = copy.copy(self.get_req.response)

    def vlt_info(self, vlt_id: int, adh_id: int):
        """Volunteer info.

        Args:
            vlt_id: volunteer id
            adh_id: adherent id of the volunteer
        """
        st.write(
            f"""## {self.json_pd_vlt.loc[vlt_id, 'firstname']} \
            {self.json_pd_vlt.loc[vlt_id, 'lastname']}"""
        )
        with st.expander("Personal info", False):
            st.write(f"- volunteer id : {vlt_id}")
            st.write(f"- adherent id : {adh_id}")
            st.write(f"- Email : {self.json_pd_vlt.loc[vlt_id, 'email']}")
            st.write(f"- Discord : {self.json_pd_vlt.loc[vlt_id, 'discord']}")
            st.write(f"- Phone : {self.json_pd_vlt.loc[vlt_id, 'phone']}")
            st.write(f"- University : {self.json_pd_vlt.loc[vlt_id, 'university']}")
            st.write(
                f"- Postal address : {self.json_pd_vlt.loc[vlt_id, 'postal_address']}"
            )
        if self.json_pd_vlt.loc[vlt_id, "actif"]:
            if self.json_pd_vlt.loc[vlt_id, "hr_status"] != "volunteer":
                position = self.json_pd_vlt.loc[vlt_id, "hr_status"]
            else:
                position = (
                    "Bureau"
                    if self.json_pd_vlt.loc[vlt_id, "bureau"]
                    else "Active member"
                )
        else:
            position = "Alumni"
        st.write(f"Actual position : {position}")
        st.write(f"Volunteer since : {self.json_pd_vlt.loc[vlt_id, 'started_date']}")

    def as_staff(self, vlt_id: int):
        """As staff history.

        Args:
            vlt_id: volunteer id
        """
        with st.expander("As staff"):
            # Events
            st.write("#### Events staff :")
            self.endpoint = f"{Endpoint.EVE_STA_VLT}/{vlt_id}"
            if self.get_req.get_data(self):
                events_json = copy.copy(self.get_req.response)
                for _, id_event in events_json["id_event"].items():
                    self.endpoint = f"{Endpoint.EVES}/{id_event}"
                    if self.get_req.get_data(self):
                        self.json_pd = json.loads(self.get_req.response)
                        st.write(f"- {self.json_pd['name']} - {self.json_pd['date']}")
            # Plannings
            st.write("#### Plannings shift :")
            self.endpoint = f"{Endpoint.PLA_ATT_VLT}/{vlt_id}"
            if self.get_req.get_data(self):
                plannings_json = copy.copy(self.get_req.response)
                for id_planning, date_planning, job_planning in zip(
                    plannings_json["id_planning"].items(),
                    plannings_json["date"].items(),
                    plannings_json["job"].items(),
                ):
                    self.endpoint = f"{Endpoint.PLAS}/{id_planning[1]}"
                    date_planning = datetime.strptime(
                        str(date_planning[1]), "%Y-%m-%d %H:%M:%S"
                    )
                    date_planning = date_planning.strftime("%Y-%m-%d")
                    job_planning = job_planning[1]
                    if self.get_req.get_data(self):
                        self.json_pd = json.loads(self.get_req.response)
                        st.write(
                            f"- {self.json_pd['name']} - {date_planning} - {job_planning}"
                        )

    def as_attendee(self, adh_id: int):
        """As attendee history.

        Args:
            adh_id: adherent id of the volunteer
        """
        with st.expander("As attendee"):
            # Events
            st.write("### Events attendee :")
            self.endpoint = f"{Endpoint.EVE_ATT_ADH}/{adh_id}"
            if self.get_req.get_data(self):
                events_json = copy.copy(self.get_req.response)
                for _, id_event in events_json["id_event"].items():
                    self.endpoint = f"{Endpoint.EVES}/{id_event}"
                    if self.get_req.get_data(self):
                        self.json_pd = json.loads(self.get_req.response)
                        st.write(f"- {self.json_pd['name']} - {self.json_pd['date']}")

    def adhesion_check(self, vlt_id: int, adh_id: int, adh_date: int):
        """Check adhesion of a single Volunteer.

        Args:
            vlt_id: volunteer id
            adh_id: adherent id of the volunteer
            adh_date: adhesion date of the volunteer
        """
        if (
            self.json_pd_vlt.loc[vlt_id, "actif"]
            and self.json_pd_vlt.loc[vlt_id, "hr_status"] == "volunteer"
        ):
            if adh_id is None:
                st.warning(
                    f"""The adhesion of {self.json_pd_vlt.loc[vlt_id, 'firstname']} \
                    {self.json_pd_vlt.loc[vlt_id, 'lastname']} has expired !"""
                )

            elif (datetime.now() - datetime.strptime(adh_date, "%Y-%m-%d")).days >= 365:
                st.warning(
                    f"""The adhesion of {self.json_pd_vlt.loc[vlt_id, 'firstname']} \
                    {self.json_pd_vlt.loc[vlt_id, 'lastname']} has expired !"""
                )
            elif (datetime.now() - datetime.strptime(adh_date, "%Y-%m-%d")).days >= 330:
                st.warning(
                    f"""The adhesion of {self.json_pd_vlt.loc[vlt_id, 'firstname']} \
                    {self.json_pd_vlt.loc[vlt_id, 'lastname']} gonna be expired very soon !"""
                )
            else:
                st.success(
                    f"""The adhesion of {self.json_pd_vlt.loc[vlt_id, 'firstname']} \
                    {self.json_pd_vlt.loc[vlt_id, 'lastname']} \
                    is up to date of the {adh_date}."""
                )

    def gen_card(self):
        """Gen card about Volunteer."""
        st.write("## Volunteer information")

        if self.json_pd_vlt is None:
            st.warning("Data is empty !")
            return

        selected_indices = st.selectbox("Select volunteer :", self.json_pd_vlt.index)
        info_vlt = st.checkbox("Info about a Volunteer ?", False, key="info_vlt")

        if info_vlt:
            selected_rows = self.json_pd_adh.loc[
                (
                    self.json_pd_adh["firstname"]
                    == self.json_pd_vlt.loc[selected_indices, "firstname"]
                )
                & (
                    self.json_pd_adh["lastname"]
                    == self.json_pd_vlt.loc[selected_indices, "lastname"]
                )
                & (
                    self.json_pd_adh["email"]
                    == self.json_pd_vlt.loc[selected_indices, "email"]
                )
            ]
            adh_id = selected_rows.index[0] if len(selected_rows) > 0 else None
            adh_date = (
                selected_rows.loc[selected_rows.index[0], "adhesion_date"]
                if len(selected_rows) > 0
                else None
            )
            self.adhesion_check(
                vlt_id=selected_indices, adh_id=adh_id, adh_date=adh_date
            )
            self.vlt_info(vlt_id=selected_indices, adh_id=adh_id)
            st.write("### History")
            self.as_staff(vlt_id=selected_indices)
            if adh_id is not None:
                self.as_attendee(adh_id=adh_id)
