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
        self.recom_adhesion_price = 5
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
        self.started_date_vlt = date(1970, 1, 1)

        # Legacy
        self.adh_data = Adherent()
        self.adh_data.get_data()

        # Adhesion check
        self.adhesion = False

    def get_data(self):
        """Get volunteer data."""
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
            f_col, l_col, b_col, a_col, ac_col, _ = st.columns([2, 2, 2, 2, 2, 5])
            fname_filter = f_col.checkbox("Firstname", False, key="vlt_fname")
            lname_filter = l_col.checkbox("Lastname", False, key="vlt_lname")
            bureau_filter = b_col.checkbox("Bureau", False, key="vlt_bureau")
            alumni_filter = a_col.checkbox("Alumni", False, key="vlt_alumni")
            actif_filter = ac_col.checkbox("Actif", not alumni_filter, key="vlt_actif")

            if alumni_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["actif"] != alumni_filter]

            if actif_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["actif"] == actif_filter]

            if bureau_filter:
                self.json_pd = self.json_pd.loc[self.json_pd["bureau"] == bureau_filter]

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

        for fname_vlt, lname_vlt, email_vlt, actif_vlt in zip(
            self.json_pd["firstname"],
            self.json_pd["lastname"],
            self.json_pd["email"],
            self.json_pd["actif"],
        ):
            if actif_vlt:
                selected_rows = self.adh_data.json_pd.loc[
                    (self.adh_data.json_pd["firstname"] == fname_vlt)
                    & (self.adh_data.json_pd["lastname"] == lname_vlt)
                    & (self.adh_data.json_pd["email"] == email_vlt)
                ]
                if len(selected_rows) <= 0:
                    st.warning(f"The adhesion of {fname_vlt} {lname_vlt} has expired !")

    def update_volunteer(self):
        """Update a volunteer."""
        st.write("## Update a volunteer")
        st.markdown(
            "If you want to auto complete most of the item, selected the `id` of the volunteer."
        )

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        up_vlt = st.checkbox("Update an Volunteer ?", False)

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
                    "Discoard pseudo", self.json_pd.loc[selected_indices, "discord"]
                )
                self.phone_vlt = st.text_input(
                    "Phoner number", self.json_pd.loc[selected_indices, "phone"]
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
