"""
#############################################
#
# 7_Volunteers.py
#
# Volunteer page
#
#############################################
"""
import streamlit as st
from controllers.volunteer import Volunteer
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Volunteer",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Volunteers")

    my_volunteers = Volunteer()
    my_volunteers.get_data()

    PAGES = {
        "Volunteer": [my_volunteers.list_volunteers, my_volunteers.info_volunteer],
    }
    selection = st.sidebar.radio(
        "Navigation volunteer", list(PAGES.keys()), label_visibility="hidden"
    )

    for page in PAGES[selection]:
        page()
        st.markdown("---")
