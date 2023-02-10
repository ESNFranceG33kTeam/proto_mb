"""
#############################################
#
# adherent.py
#
# object for adherent call
#
#############################################
"""
from datetime import date
from datetime import datetime
import streamlit as st
from system import Call
from controllers.money import Money
from helpers import Configuration, Endpoint


class Adherent:
    """Adherent class.
    Everything about adherent object.
    """

    def __init__(self):
        """Init Adherent object."""
        self.endpoint = Endpoint.ADHS
        self.json_pd = None
        self.recom_adhesion_price = Configuration().adhesion_price
        self.label = "adherent"
        self.req_code = 0

        # Put/Post adherent
        self.id_adh = 0
        self.firstname_adh = ""
        self.lastname_adh = ""
        self.email_adh = ""
        self.dateofbirth_adh = date(1970, 1, 1)
        self.situation_adh = ""
        self.university_adh = ""
        self.homeland_adh = ""
        self.speakabout_adh = ""
        self.newsletter_adh = False
        self.adhesion_date = date.today()
        self.adhesion_price_adh = self.recom_adhesion_price

    def get_data(self) -> True:
        """Get adherent data."""
        get_req = Call()
        to_return = get_req.get_data(self)
        self.json_pd.drop(columns=["created_at"], inplace=True)
        self.json_pd.drop(columns=["updated_at"], inplace=True)
        return to_return

    def post_put_data(self, protocol: str):
        """Post or put adherent data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_req = Call()
        payload = {
            "firstname": f"{self.firstname_adh}",
            "lastname": f"{self.lastname_adh}",
            "email": f"{self.email_adh}",
            "dateofbirth": f"{self.dateofbirth_adh}",
            "situation": self.situation_adh,
            "university": f"{self.university_adh}",
            "homeland": f"{self.homeland_adh}",
            "speakabout": f"{self.speakabout_adh}",
            "newsletter": self.newsletter_adh,
            "adhesion_date": f"{self.adhesion_date}",
        }
        post_put_req.post_put_data(obj=self, payload=payload, protocol=protocol)

    def list_adherents(self):
        """List adherents."""
        st.write("## List of Adherents !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", False, key="adh_search")
        if s_filter:
            f_col, l_col, _ = st.columns([1, 1, 5])
            fname_filter = f_col.checkbox("Firstname", True, key="adh_fname")
            lname_filter = l_col.checkbox("Lastname", False, key="adh_lname")

            selected_firstname = st.selectbox(
                "Select firstname :",
                self.json_pd["firstname"],
                disabled=not fname_filter,
                key="adh_sfname",
            )
            selected_lastname = st.selectbox(
                "Select lastname :",
                self.json_pd["lastname"],
                disabled=not lname_filter,
                key="adh_slname",
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

            data_adh = selected_rows
        else:
            data_adh = self.json_pd

        st.write(data_adh)

    def update_adherent(self):
        """Update an adherent to the api."""
        st.write("## Update an Adherent")
        st.markdown(
            "If you want to auto complete most of the item, selected the `id` of the adherent."
        )

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        up_adh = st.checkbox("Update an Adherent ?", False)

        if up_adh:
            selected_indices = st.selectbox("Select rows:", self.json_pd.index)

            with st.form("Update", clear_on_submit=False):
                self.id_adh = selected_indices
                self.firstname_adh = st.text_input(
                    "Firstname", self.json_pd.loc[selected_indices, "firstname"]
                )
                self.lastname_adh = st.text_input(
                    "Lastname", self.json_pd.loc[selected_indices, "lastname"]
                )
                self.email_adh = st.text_input(
                    "Email", self.json_pd.loc[selected_indices, "email"]
                )
                date_format = datetime.strptime(
                    self.json_pd.loc[selected_indices, "dateofbirth"], "%Y-%m-%d"
                )
                self.dateofbirth_adh = st.date_input("Date of birth", date_format)
                self.situation_adh = st.selectbox(
                    "Situation",
                    Configuration().adh_situation,
                    Configuration().adh_situation.index(
                        self.json_pd.loc[selected_indices, "situation"]
                    ),
                    key="adh_situation",
                )
                self.university_adh = st.selectbox(
                    "University",
                    Configuration().universities,
                    Configuration().universities.index(
                        self.json_pd.loc[selected_indices, "university"]
                    ),
                    key="adh_university",
                )
                self.homeland_adh = st.selectbox(
                    "Homeland",
                    Configuration().countries,
                    Configuration().countries.index(
                        self.json_pd.loc[selected_indices, "homeland"]
                    ),
                    key="adh_homeland",
                )
                self.speakabout_adh = st.text_input(
                    "How does he learn about us ?",
                    self.json_pd.loc[selected_indices, "speakabout"],
                )
                self.newsletter_adh = st.checkbox(
                    "Newsletter ?", self.json_pd.loc[selected_indices, "newsletter"]
                )
                date_format = datetime.strptime(
                    self.json_pd.loc[selected_indices, "adhesion_date"], "%Y-%m-%d"
                )
                self.adhesion_date = st.date_input(
                    "Adhesion date", date_format, disabled=True
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if self.id_adh != 0 and len(self.firstname_adh) > 0:
                        self.post_put_data(protocol="put")
                        if self.req_code == 200:
                            st.success("Adherent updated ✌️")
                    else:
                        st.warning(
                            """
                            You forget some info...

                            The `firstname`, `lastname` are **MANDATORY**.
                            """
                        )

    def new_adherent(self):
        """Create a new adherent."""
        st.write("## Create a new Adherent")

        with st.form("New adherent", clear_on_submit=True):
            self.firstname_adh = st.text_input("Firstname")
            self.lastname_adh = st.text_input("Lastname")
            self.email_adh = st.text_input("Email")
            self.dateofbirth_adh = st.date_input(
                "Date of birth", self.dateofbirth_adh, max_value=date.today()
            )
            self.situation_adh = st.selectbox(
                "Situation", Configuration().adh_situation
            )
            self.university_adh = st.selectbox(
                "University", Configuration().universities
            )
            self.homeland_adh = st.selectbox("Homeland", Configuration().countries)
            self.speakabout_adh = st.text_input("How does she/he learned about us ?")

            self.adhesion_date = st.date_input(
                "Adhesion date", value=date.today(), max_value=date.today()
            )

            st.markdown("---")
            self.newsletter_adh = st.checkbox("Newsletter")
            terms_adh = st.checkbox("I declare to accept the terms and conditions.")
            self.adhesion_price_adh = st.number_input(
                f"Adhesion price, the recommended price is {self.recom_adhesion_price}€",
                value=self.recom_adhesion_price,
            )
            payment_type = st.selectbox("Payment type", Configuration().money_type)

            submitted = st.form_submit_button("Submit")
            if submitted:
                if terms_adh and (
                    len(self.firstname_adh) > 0 and len(self.lastname_adh) > 0
                ):
                    # Post adherent
                    self.post_put_data(protocol="post")
                    if self.adhesion_price_adh > 0:
                        # Post money
                        adh_money = Money()
                        adh_money.label = self.label
                        adh_money.price = self.adhesion_price_adh
                        adh_money.payment_type = payment_type
                        adh_money.payment_date = self.adhesion_date
                        adh_money.post_data()
                    else:
                        adh_money = Money()
                        adh_money.req_code = 200

                    if self.req_code == 200 and adh_money.req_code == 200:
                        st.success("Adherent and money operation added ✌️")
                    else:
                        error_add_adh = (
                            "Add adherent : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add adherent : OK"
                        )
                        error_add_mon = (
                            "Add money operation : " + str(adh_money.req_code)
                            if adh_money.req_code != 200
                            else "Add money operation : OK"
                        )
                        st.error(f"{error_add_adh} | {error_add_mon}")
                else:
                    st.warning(
                        """
                        You forget some info...

                        The `firstname`, `lastname`, `terms and conditions` are **MANDATORY**.
                        """
                    )

    def renew_adherent(self):
        """Renew an adherent to the api."""
        st.write("## Renew adhesion")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        re_adh = st.checkbox("Renew an Adherent ?", False)

        if re_adh:
            selected_indices = st.selectbox("Select rows:", self.json_pd.index)

            with st.form("Renew", clear_on_submit=False):
                self.id_adh = selected_indices
                self.firstname_adh = st.text_input(
                    "Firstname",
                    self.json_pd.loc[selected_indices, "firstname"],
                    disabled=True,
                )
                self.lastname_adh = st.text_input(
                    "Lastname",
                    self.json_pd.loc[selected_indices, "lastname"],
                    disabled=True,
                )
                self.email_adh = st.text_input(
                    "Email", self.json_pd.loc[selected_indices, "email"], disabled=True
                )
                self.dateofbirth_adh = self.json_pd.loc[selected_indices, "dateofbirth"]
                self.situation_adh = st.selectbox(
                    "Situation",
                    Configuration().adh_situation,
                    Configuration().adh_situation.index(
                        self.json_pd.loc[selected_indices, "situation"]
                    ),
                    key="adh_situation",
                )
                self.university_adh = self.json_pd.loc[selected_indices, "university"]
                self.homeland_adh = self.json_pd.loc[selected_indices, "homeland"]
                self.speakabout_adh = self.json_pd.loc[selected_indices, "speakabout"]
                self.newsletter_adh = st.checkbox(
                    "Newsletter ?", self.json_pd.loc[selected_indices, "newsletter"]
                )
                self.adhesion_date = st.date_input(
                    "Adhesion date", value=date.today(), max_value=date.today()
                )
                self.adhesion_price_adh = st.number_input(
                    f"Adhesion price, the recommended price is {self.recom_adhesion_price}€",
                    value=self.recom_adhesion_price,
                )
                payment_type = st.selectbox("Payment type", Configuration().money_type)

                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Put adherent
                    self.post_put_data(protocol="put")
                    if self.adhesion_price_adh > 0:
                        # Post money
                        adh_money = Money()
                        adh_money.label = self.label
                        adh_money.price = self.adhesion_price_adh
                        adh_money.payment_type = payment_type
                        adh_money.payment_date = self.adhesion_date
                        adh_money.post_data()
                    else:
                        adh_money = Money()
                        adh_money.req_code = 200

                    if self.req_code == 200 and adh_money.req_code == 200:
                        st.success("Adherent and money operation added ✌️")
                    else:
                        error_add_adh = (
                            "Renew adherent : " + str(self.req_code)
                            if self.req_code != 200
                            else "Renew adherent : OK"
                        )
                        error_add_mon = (
                            "Add money operation : " + str(adh_money.req_code)
                            if adh_money.req_code != 200
                            else "Add money operation : OK"
                        )
                        st.error(f"{error_add_adh} | {error_add_mon}")
