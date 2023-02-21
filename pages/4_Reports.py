"""
#############################################
#
# 4_Reports.py
#
# Report page
#
#############################################
"""
import streamlit as st
from controllers.report import Report
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Report",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Reports")

    my_reports = Report()

    PAGES = {
        "View": [my_reports.list_reports, my_reports.read_report],
    }
    selection = st.sidebar.radio(
        "Navigation report", list(PAGES.keys()), label_visibility="hidden"
    )

    for page in PAGES[selection]:
        page()
        st.markdown("---")
