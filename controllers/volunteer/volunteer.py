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
import copy
from datetime import date, datetime
import pandas as pd
import streamlit as st
from system import Call
from helpers import Configuration
from controllers.adherent import Adherent


class Volunteer:
    """Volunteer class.
    Everything about volunteer object.
    """

    def __init__(self):
        """Init Volunteer object."""
        self.endpoint = "auth/volunteers"
        self.json_pd = None
        self.recom_adhesion_price = 1
        self.label = "volunteer"
        self.req_code = 0

        # Put/Post volunteer
        self.id_vlt = 0
        self.firstname_vlt = ""
        self.lastname_vlt = ""
        self.email_vlt = ""
        self.discord_vlt = ""
        self.phone_vlt = "+33 0123456789"
        self.university_vlt = ""
        self.postal_address_vlt = ""
        self.actif = False
        self.bureau = False
        self.employee = False
        self.started_date_vlt = date(1970, 1, 1)

        # Legacy
        self.adh_data = Adherent()
        self.adh_data.get_data()

        # Adhesion check
        self.adhesion = False

    def get_data(self) -> True:
        """Get volunteer data.

        Return:
            True/None
        """
        get_list = Call()

        get_list.req_url(endpoint=self.endpoint, protocol="get")
        self.req_code = get_list.status_code

        if get_list.status_code != 200:
            st.warning(get_list.error)
            return

        if get_list.response is None:
            return

        if type(get_list.response) is list:
            json_dec = json.dumps(get_list.response)
            self.json_pd = pd.read_json(json_dec)
            self.json_pd.set_index("id", inplace=True)
        else:
            self.json_pd = json.dumps(get_list.response)
        return True

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
            "discord": f"{self.discord_vlt}",
            "phone": f"{self.phone_vlt}",
            "university": f"{self.university_vlt}",
            "postal_address": f"{self.postal_address_vlt}",
            "actif": self.actif,
            "bureau": self.bureau,
            "employee": self.employee,
            "started_date": f"{self.started_date_vlt}",
        }

        if protocol == "put":
            self.endpoint = self.endpoint + "/" + str(self.id_vlt)

        post_put_vlt.req_url(endpoint=self.endpoint, data=data, protocol=protocol)
        self.req_code = post_put_vlt.status_code

        if post_put_vlt.status_code != 200:
            st.warning(post_put_vlt.error)

    def list_volunteers(self):
        """List all volunteers."""
        st.write("## List of Volunteers !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", False, key="vlt_search")
        if s_filter:
            f_col, l_col, b_col, a_col, e_col, ac_col, _ = st.columns(
                [3, 3, 3, 3, 3, 3, 5]
            )
            fname_filter = f_col.checkbox("Firstname", False, key="vlt_fname")
            lname_filter = l_col.checkbox("Lastname", False, key="vlt_lname")
            bureau_filter = b_col.checkbox("Bureau", False, key="vlt_bureau")
            employee_filter = e_col.checkbox("Employee", False, key="vlt_employee")
            alumni_filter = a_col.checkbox("Alumni", False, key="vlt_alumni")
            actif_filter = ac_col.checkbox("Actif", not alumni_filter, key="vlt_actif")

            if alumni_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["actif"] != alumni_filter]

            if actif_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["actif"] == actif_filter]

            if bureau_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["bureau"] == bureau_filter]

            if employee_filter:
                self.json_pd = self.json_pd.loc[
                    self.json_pd["employee"] == employee_filter
                ]

            selected_firstname = st.selectbox(
                "Select firstname :",
                self.json_pd["firstname"],
                disabled=not fname_filter,
                key="vlt_sfname",
            )
            selected_lastname = st.selectbox(
                "Select lastname :",
                self.json_pd["lastname"],
                disabled=not lname_filter,
                key="vlt_slname",
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

    def check_adhesion(self):
        """Check the adhesion of the active volunteers."""
        st.write("## Adhesion checker")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        for fname_vlt, lname_vlt, email_vlt, actif_vlt, employee_vlt in zip(
            self.json_pd["firstname"],
            self.json_pd["lastname"],
            self.json_pd["email"],
            self.json_pd["actif"],
            self.json_pd["employee"],
        ):
            if actif_vlt and not employee_vlt:
                selected_rows = self.adh_data.json_pd.loc[
                    (self.adh_data.json_pd["firstname"] == fname_vlt)
                    & (self.adh_data.json_pd["lastname"] == lname_vlt)
                    & (self.adh_data.json_pd["email"] == email_vlt)
                ]
                adh_date = (
                    selected_rows.loc[selected_rows.index[0], "adhesion_date"]
                    if len(selected_rows) > 0
                    else None
                )
                if len(selected_rows) <= 0:
                    st.warning(f"The adhesion of {fname_vlt} {lname_vlt} has expired !")
                elif (
                    datetime.now() - datetime.strptime(adh_date, "%Y-%m-%d")
                ).days >= 365:
                    st.warning(f"The adhesion of {fname_vlt} {lname_vlt} has expired !")

    def info_volunteer(self):
        """Get the info about a volunteer."""
        st.write("## Volunteer information")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        selected_indices = st.selectbox("Select volunteer :", self.json_pd.index)
        info_vlt = st.checkbox("Info about a Volunteer ?", False, key="info_vlt")

        if info_vlt:
            st.write(
                f"""## {self.json_pd.loc[selected_indices, 'firstname']} \
                {self.json_pd.loc[selected_indices, 'lastname']}"""
            )
            selected_rows = self.adh_data.json_pd.loc[
                (
                    self.adh_data.json_pd["firstname"]
                    == self.json_pd.loc[selected_indices, "firstname"]
                )
                & (
                    self.adh_data.json_pd["lastname"]
                    == self.json_pd.loc[selected_indices, "lastname"]
                )
                & (
                    self.adh_data.json_pd["email"]
                    == self.json_pd.loc[selected_indices, "email"]
                )
            ]
            adh_id = selected_rows.index[0] if len(selected_rows) > 0 else None
            adh_date = (
                selected_rows.loc[selected_rows.index[0], "adhesion_date"]
                if len(selected_rows) > 0
                else None
            )

            # Adhesion check
            if (
                self.json_pd.loc[selected_indices, "actif"]
                and not self.json_pd.loc[selected_indices, "employee"]
            ):
                if len(selected_rows) <= 0:
                    st.warning(
                        f"""The adhesion of {self.json_pd.loc[selected_indices, 'firstname']} \
                        {self.json_pd.loc[selected_indices, 'lastname']} has expired !"""
                    )

                elif (
                    datetime.now() - datetime.strptime(adh_date, "%Y-%m-%d")
                ).days >= 365:
                    st.warning(
                        f"""The adhesion of {self.json_pd.loc[selected_indices, 'firstname']} \
                        {self.json_pd.loc[selected_indices, 'lastname']} has expired !"""
                    )

            # Personal info
            with st.expander("Personal info", False):
                st.write(f"- volunteer id : {selected_indices}")
                st.write(f"- adherent id : {adh_id}")
                st.write(f"- Email : {self.json_pd.loc[selected_indices, 'email']}")
                st.write(f"- Discord : {self.json_pd.loc[selected_indices, 'discord']}")
                st.write(f"- Phone : {self.json_pd.loc[selected_indices, 'phone']}")
                st.write(
                    f"- University : {self.json_pd.loc[selected_indices, 'university']}"
                )
                st.write(
                    f"- Postal address : {self.json_pd.loc[selected_indices, 'postal_address']}"
                )
            if self.json_pd.loc[selected_indices, "actif"]:
                if self.json_pd.loc[selected_indices, "employee"]:
                    position = "Employee"
                else:
                    position = (
                        "Bureau"
                        if self.json_pd.loc[selected_indices, "bureau"]
                        else "Active member"
                    )
            else:
                position = "Alumni"
            # Volunteer status
            st.write(f"Actual position : {position}")
            st.write(
                f"Volunteer since : {self.json_pd.loc[selected_indices, 'started_date']}"
            )
            st.write("---")

            # History
            st.write("### History")
            with st.expander("As staff"):
                st.write("#### Events staff :")
                self.endpoint = f"auth/event_staffs/id_volunteer/{selected_indices}"
                if self.get_data():
                    events_json = copy.copy(self.json_pd)
                    for _, id_event in events_json["id_event"].items():
                        self.endpoint = f"auth/events/{id_event}"
                        if self.get_data():
                            self.json_pd = json.loads(self.json_pd)
                            st.write(
                                f"- {self.json_pd['name']} - {self.json_pd['date']}"
                            )
                st.write("#### Plannings shift :")
                self.endpoint = (
                    f"auth/planning_attendees/id_volunteer/{selected_indices}"
                )
                if self.get_data():
                    plannings_json = copy.copy(self.json_pd)
                    for id_planning, date_planning, job_planning in zip(
                        plannings_json["id_planning"].items(),
                        plannings_json["date"].items(),
                        plannings_json["job"].items(),
                    ):
                        self.endpoint = f"auth/plannings/{id_planning[1]}"
                        date_planning = datetime.strptime(
                            str(date_planning[1]), "%Y-%m-%d %H:%M:%S"
                        )
                        date_planning = date_planning.strftime("%Y-%m-%d")
                        job_planning = job_planning[1]
                        if self.get_data():
                            self.json_pd = json.loads(self.json_pd)
                            st.write(
                                f"- {self.json_pd['name']} - {date_planning} - {job_planning}"
                            )

            if adh_id is not None:
                with st.expander("As attendee"):
                    st.write("### Events attendee :")
                    self.endpoint = f"auth/event_attendees/id_adherent/{adh_id}"
                    if self.get_data():
                        events_json = copy.copy(self.json_pd)
                        for _, id_event in events_json["id_event"].items():
                            self.endpoint = f"auth/events/{id_event}"
                            if self.get_data():
                                self.json_pd = json.loads(self.json_pd)
                                st.write(
                                    f"- {self.json_pd['name']} - {self.json_pd['date']}"
                                )

    def update_volunteer(self):
        """Update a volunteer."""
        st.write("## Update a volunteer")
        st.markdown(
            "If you want to auto complete most of the item, selected the `id` of the volunteer."
        )

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        up_vlt = st.checkbox("Update an Volunteer ?", False, key="up_vlt")

        if up_vlt:
            selected_indices = st.selectbox("Select adherent :", self.json_pd.index)

            with st.form("Update a volunteer", clear_on_submit=False):
                self.id_vlt = selected_indices
                self.firstname_vlt = st.text_input(
                    "Firstname", self.json_pd.loc[selected_indices, "firstname"]
                )
                self.lastname_vlt = st.text_input(
                    "Lastname", self.json_pd.loc[selected_indices, "lastname"]
                )
                self.email_vlt = st.text_input(
                    "Email", self.json_pd.loc[selected_indices, "email"]
                )
                self.discord_vlt = st.text_input(
                    "Discord pseudo", self.json_pd.loc[selected_indices, "discord"]
                )
                self.phone_vlt = st.text_input(
                    "Phone number", self.json_pd.loc[selected_indices, "phone"]
                )
                self.university_vlt = st.selectbox(
                    "University",
                    Configuration().universities,
                    Configuration().universities.index(
                        self.json_pd.loc[selected_indices, "university"]
                    ),
                )
                self.postal_address_vlt = st.text_input(
                    "Postal address",
                    self.json_pd.loc[selected_indices, "postal_address"],
                )
                self.bureau = st.checkbox(
                    "Bureau ?", self.json_pd.loc[selected_indices, "bureau"]
                )
                self.actif = not (
                    st.checkbox(
                        "Alumni ?", not (self.json_pd.loc[selected_indices, "actif"])
                    )
                )
                date_format = datetime.strptime(
                    self.json_pd.loc[selected_indices, "started_date"], "%Y-%m-%d"
                )
                self.started_date_vlt = st.date_input(
                    "Date of volunteering started",
                    value=date_format,
                    max_value=date.today(),
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Put volunteer
                    self.post_put_data(protocol="put")

                    if self.req_code == 200:
                        st.success("Volunteer updated ✌️")
                    else:
                        error_add_vlt = (
                            "Add Volunteer : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add Volunteer : OK"
                        )
                        st.error(f"{error_add_vlt}")

    def new_volunteer(self):
        """Add a new volunteer."""
        st.write("## New volunteer")
        st.markdown("To add a new volunteer, the person has to be an adherent first.")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        new_vlt = st.checkbox("New Volunteer ?", False, key="new_vlt")

        if new_vlt:
            selected_indices = st.selectbox(
                "Select adherent :", self.adh_data.json_pd.index, key="adh_indice"
            )

            with st.form("New volunteer", clear_on_submit=False):
                self.firstname_vlt = st.text_input(
                    "Firstname",
                    self.adh_data.json_pd.loc[selected_indices, "firstname"],
                    disabled=True,
                )
                self.lastname_vlt = st.text_input(
                    "Lastname",
                    self.adh_data.json_pd.loc[selected_indices, "lastname"],
                    disabled=True,
                )
                self.email_vlt = st.text_input(
                    "Email",
                    self.adh_data.json_pd.loc[selected_indices, "email"],
                    disabled=True,
                )
                self.discord_vlt = st.text_input("Discord pseudo")

                col_indic, col_number = st.columns([1, 5], gap="small")
                indic_phone = col_indic.selectbox(
                    "Indicatif",
                    Configuration().indicative,
                    Configuration().indicative.index("+33"),
                )
                number_phone = col_number.text_input("Phone number")

                self.university_vlt = st.selectbox(
                    "University",
                    Configuration().universities,
                    Configuration().universities.index(
                        self.adh_data.json_pd.loc[selected_indices, "university"]
                    ),
                    key="vlt_university",
                )
                self.postal_address_vlt = st.text_input("Postal address")

                st.markdown("---")
                _ = st.checkbox("Volunteer ?", True, disabled=True)
                self.bureau = st.checkbox("Bureau ?", False)
                self.actif = not st.checkbox("Alumni ?", False)
                self.started_date_vlt = st.date_input(
                    "Date of volunteering started",
                    value=date.today(),
                    max_value=date.today(),
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Post volunteer
                    if number_phone[0] != "0":
                        number_phone = f"0{number_phone}"
                    self.phone_vlt = f"{indic_phone} {number_phone}"

                    self.post_put_data(protocol="post")

                    if self.req_code == 200:
                        st.success("Volunteer added ✌️")
                    else:
                        error_add_vlt = (
                            "Add Volunteer : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add Volunteer : OK"
                        )
                        st.error(f"{error_add_vlt}")

    def new_employee(self):
        """Add a new employee."""
        st.write("## New employee")
        st.markdown("To add a new employee.")

        new_emp = st.checkbox("New Employee ?", False, key="new_emp")

        if new_emp:
            with st.form("New employee", clear_on_submit=False):
                self.firstname_vlt = st.text_input("Firstname")
                self.lastname_vlt = st.text_input("Lastname")
                self.email_vlt = st.text_input("Email")
                self.discord_vlt = st.text_input("Discord pseudo")

                col_indic, col_number = st.columns([1, 5], gap="small")
                indic_phone = col_indic.selectbox(
                    "Indicatif",
                    Configuration().indicative,
                    Configuration().indicative.index("+33"),
                )
                number_phone = col_number.text_input("Phone number")

                self.university_vlt = st.selectbox(
                    "University",
                    Configuration().universities,
                    Configuration().universities.index("activité pro"),
                )
                self.postal_address_vlt = st.text_input("Postal address")

                st.markdown("---")
                self.bureau = False
                self.actif = True
                self.employee = True
                self.started_date_vlt = st.date_input(
                    "Date of employment started",
                    value=date.today(),
                    max_value=date.today(),
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Post volunteer
                    if number_phone[0] != "0":
                        number_phone = f"0{number_phone}"
                    self.phone_vlt = f"{indic_phone} {number_phone}"

                    self.post_put_data(protocol="post")

                    if self.req_code == 200:
                        st.success("Employee added ✌️")
                    else:
                        error_add_vlt = (
                            "Add Employee : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add Employee : OK"
                        )
                        st.error(f"{error_add_vlt}")
