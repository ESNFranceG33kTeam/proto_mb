"""
#############################################
#
# report.py
#
# object for report call
#
#############################################
"""
from datetime import date, datetime
import pandas as pd
import streamlit as st
from system import Call
from helpers import Configuration, Endpoint


class Report:
    """Report class.
    Everything about report object.
    """

    def __init__(self):
        """Init report object."""
        self.endpoint = Endpoint.RPTS
        self.json_pd = None
        self.label = "report"
        self.req_code = 0
        self.get_data()

        # Put/Post report
        self.id = 0
        self.type_rpt = "custom"
        self.refext_rpt = 0
        self.name_rpt = ""
        self.date_rpt = date(1970, 1, 1)
        self.comment_rpt = ""
        self.nb_reel_att = 0
        self.nb_subs_att = 0
        self.staffs_list = ""
        self.nb_hours_prepa = 0
        self.nb_hours = 0
        self.nb_staffs = 0
        self.taux_valo = Configuration().taux_smic
        self.code_public = "ALL"
        self.code_project = ""

    def get_data(self) -> True:
        """Get report data.

        Return:
            True/None
        """
        get_req = Call()
        to_return = get_req.get_data(self)
        self.req_code = get_req.status_code
        self.json_pd = get_req.response
        self.json_pd["date"] = pd.to_datetime(self.json_pd["date"])
        self.json_pd["date"] = self.json_pd["date"].dt.strftime("%Y-%m-%d")
        return to_return

    def post_put_data(self, protocol: str):
        """Post or put report data.

        Args:
            protocol: protocol to use, can be `post` or `put`
        """
        post_put_req = Call()
        payload = {
            "type": f"{self.type_rpt}",
            "ref_ext": self.refext_rpt,
            "name": f"{self.name_rpt}",
            "date": f"{self.date_rpt}",
            "comment": f"{self.comment_rpt}",
            "nb_reel_attendees": f"{self.nb_reel_att}",
            "nb_subscribe_attendees": f"{self.nb_subs_att}",
            "staffs_list": f"{self.staffs_list}",
            "nb_hours_prepa": f"{self.nb_hours_prepa}",
            "nb_hours": f"{self.nb_hours}",
            "nb_staffs": f"{self.nb_hours}",
            "taux_valorisation": f"{self.taux_valo}",
            "code_public": f"{self.code_public}",
            "code_project": f"{self.code_project}",
        }
        post_put_req.post_put_data(obj=self, payload=payload, protocol=protocol)
        self.req_code = post_put_req.status_code

    def list_reports(self):
        """List all reports."""
        st.write("## List of Reports !")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        s_filter = st.checkbox("Search filters", False, key="rpt_search")
        if s_filter:
            n_col, t_col, _ = st.columns(
                [3, 3, 5]
            )
            name_filter = n_col.checkbox("Name", False, key="rpt_name")
            type_filter = t_col.checkbox("Type", False, key="rpt_type")

            selected_name = st.selectbox(
                "Select name :",
                self.json_pd["name"],
                disabled=not name_filter,
                key="rpt_sname",
            )
            selected_type = st.selectbox(
                "Select type :",
                Configuration().report_types,
                disabled=not type_filter,
                key="rpt_stype",
            )

            s_name = selected_name if name_filter else ""
            s_type = selected_type if type_filter else ""

            if name_filter and type_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["name"] == s_name)
                    & (self.json_pd["type"] == s_type)
                ]
            elif name_filter or type_filter:
                selected_rows = self.json_pd.loc[
                    (self.json_pd["name"] == s_name)
                    | (self.json_pd["type"] == s_type)
                ]
            else:
                selected_rows = self.json_pd

            data_rpt = selected_rows
        else:
            data_rpt = self.json_pd

        df_print = data_rpt.drop('ref_ext', axis=1)
        df_print.drop('comment', axis=1, inplace=True)
        df_print.drop('staffs_list', axis=1, inplace=True)
        st.write(df_print)

    def read_report(self):
        """Read a report."""
        st.write("## Read a report")
        st.markdown(
            "Select the `id` of the report to read."
        )

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        rpt_id = st.selectbox("Select volunteer :", self.json_pd.index)
        read_rpt = st.checkbox("Read a Report ?", False, key="read_rpt")

        if read_rpt:
            ref_ext = self.json_pd.loc[rpt_id, 'ref_ext']
            nb_subs_att = self.json_pd.loc[rpt_id, 'nb_subscribe_attendees']
            taux_valo = self.json_pd.loc[rpt_id, 'taux_valorisation']
            nb_hours = self.json_pd.loc[rpt_id, 'nb_hours']
            nb_hours_prepa = self.json_pd.loc[rpt_id, 'nb_hours_prepa']

            st.write(f"## {self.json_pd.loc[rpt_id, 'name']}")
            st.write(f"- Date : {self.json_pd.loc[rpt_id, 'date']}")
            st.write(f"- Comment : {self.json_pd.loc[rpt_id, 'comment']}")
            st.write(f"""- Nb of reel attendees : \
                    {self.json_pd.loc[rpt_id, 'nb_reel_attendees']}""")
            st.write(f"- Nb of Subscribe attendees : {nb_subs_att}") if nb_subs_att != 0 else None
            with st.expander("Administrative", True):
                st.write(f"- Type of report : {self.json_pd.loc[rpt_id, 'type']}")
                st.write(f"- External ref : {ref_ext}") if ref_ext != 0 else None
                st.write(f"- Code public : {self.json_pd.loc[rpt_id, 'code_public']}")
                st.write(f"- Code project : {self.json_pd.loc[rpt_id, 'code_project']}")
            with st.expander("Valorisation", True):
                st.write(f"- Staffs : {self.json_pd.loc[rpt_id, 'staffs_list']}")
                st.write(f"- Nb staffs : {self.json_pd.loc[rpt_id, 'nb_staffs']}")
                st.write(f"- Nb hours of preparation : {nb_hours_prepa}h")
                st.write(f"- Nb hours : {self.json_pd.loc[rpt_id, 'nb_hours']}h")
                st.write(f"- Nb hours total : {nb_hours + nb_hours_prepa} h")
                st.write(f"- Taux valorisation : {taux_valo}€")
                st.write(f"- Valorisation total : {taux_valo * nb_hours}€")

    def update_report(self):
        """Update a report."""
        st.write("## Update a report")
        st.markdown(
            "If you want to auto complete most of the item, selected the `id` of the report."
        )

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        up_rpt = st.checkbox("Update a Report ?", False, key="up_rpt")

        if up_rpt:
            selected_indices = st.selectbox("Select report :", self.json_pd.index)

            with st.form("Update a report", clear_on_submit=False):
                self.id = selected_indices
                self.name_rpt = st.text_input(
                    "Name", self.json_pd.loc[selected_indices, "name"]
                )
                date_format = datetime.strptime(
                    self.json_pd.loc[selected_indices, "date"], "%Y-%m-%d"
                )
                self.date_rpt = st.date_input(
                    "Date of the event/planning/custom started",
                    value=date_format,
                    max_value=date.today(),
                )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Put volunteer
                    self.post_put_data(protocol="put")

                    if self.req_code == 200:
                        st.success("Report updated ✌️")
                    else:
                        error_add_rpt = (
                            "Add Report : " + str(self.req_code)
                            if self.req_code != 200
                            else "Add Report : OK"
                        )
                        st.error(f"{error_add_rpt}")

    def new_report(self):
        """Add a new report."""
        st.write("## New report")
        st.markdown("You can create new Report from an event, planning or from scratch.")

        if self.json_pd is None:
            st.warning("Data is empty !")
            return

        new_rpt = st.checkbox("New Report ?", False, key="new_rpt")

        # if new_vlt:
        #     selected_indices = st.selectbox(
        #         "Select adherent :", self.adh_data.json_pd.index, key="adh_indice"
        #     )
        #
        #     with st.form("New volunteer", clear_on_submit=False):
        #         self.firstname_vlt = st.text_input(
        #             "Firstname",
        #             self.adh_data.json_pd.loc[selected_indices, "firstname"],
        #             disabled=True,
        #         )
        #         self.lastname_vlt = st.text_input(
        #             "Lastname",
        #             self.adh_data.json_pd.loc[selected_indices, "lastname"],
        #             disabled=True,
        #         )
        #         self.email_vlt = st.text_input(
        #             "Email",
        #             self.adh_data.json_pd.loc[selected_indices, "email"],
        #             disabled=True,
        #         )
        #         self.discord_vlt = st.text_input("Discord pseudo")
        #
        #         col_indic, col_number = st.columns([1, 5], gap="small")
        #         indic_phone = col_indic.selectbox(
        #             "Indicatif",
        #             Configuration().indicative,
        #             Configuration().indicative.index("+33"),
        #         )
        #         number_phone = col_number.text_input("Phone number")
        #
        #         self.university_vlt = st.selectbox(
        #             "University",
        #             Configuration().universities,
        #             Configuration().universities.index(
        #                 self.adh_data.json_pd.loc[selected_indices, "university"]
        #             ),
        #             key="vlt_university",
        #         )
        #         self.postal_address_vlt = st.text_input("Postal address")
        #
        #         st.markdown("---")
        #         _ = st.checkbox("Volunteer ?", True, disabled=True)
        #         self.bureau = st.checkbox("Bureau ?", False)
        #         self.actif = not st.checkbox("Alumni ?", False)
        #         self.started_date_vlt = st.date_input(
        #             "Date of volunteering started",
        #             value=date.today(),
        #             max_value=date.today(),
        #         )
        #
        #         submitted = st.form_submit_button("Submit")
        #         if submitted:
        #             # Post volunteer
        #             if number_phone[0] != "0":
        #                 number_phone = f"0{number_phone}"
        #             self.phone_vlt = f"{indic_phone} {number_phone}"
        #
        #             self.post_put_data(protocol="post")
        #
        #             if self.req_code == 200:
        #                 st.success("Volunteer added ✌️")
        #             else:
        #                 error_add_vlt = (
        #                     "Add Volunteer : " + str(self.req_code)
        #                     if self.req_code != 200
        #                     else "Add Volunteer : OK"
        #                 )
        #                 st.error(f"{error_add_vlt}")
