"""
#############################################
#
# 8_Bureau.py
#
# Bureau page
#
#############################################
"""
import streamlit as st
from controllers.money import Money
from controllers.volunteer import Volunteer
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Bureau",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():
    getuserlog().check_perm("bureau")

    st.write("# Bureau")

    my_volunteers = Volunteer()
    my_volunteers.get_data()

    my_adherents = my_volunteers.adh_data

    my_moneys = Money()
    my_moneys.get_data()

    PAGES = {
        "Volunteer": [
            my_volunteers.check_adhesion,
            my_volunteers.list_volunteers,
            my_volunteers.update_volunteer,
            my_adherents.list_adherents,
            my_volunteers.new_volunteer,
        ],
        "Money": [my_moneys.list_moneys, my_moneys.new_money],
    }
    selection = st.sidebar.radio(
        "Navigation bureau", list(PAGES.keys()), label_visibility="hidden"
    )

    for page in PAGES[selection]:
        page()
        st.markdown("---")
