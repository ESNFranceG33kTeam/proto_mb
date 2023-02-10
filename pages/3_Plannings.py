"""
#############################################
#
# 3_Plannings.py
#
# Plannings page
#
#############################################
"""
import streamlit as st
from controllers.planning import Planning, Attendee
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Planning",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Plannings")

    my_planings = Planning()
    my_attendees = Attendee()

    PAGES = {
        "View": [my_planings.view_planning],
        "List": [my_planings.list_plannings, my_planings.update_planning],
        "New": [my_planings.new_planning],
        "Attendee": [my_attendees.list_attendees, my_attendees.cal_attendees],
    }
    selection = st.sidebar.radio(
        "Navigation planning", list(PAGES.keys()), label_visibility="hidden"
    )

    for page in PAGES[selection]:
        page()
        st.markdown("---")

    if selection == "Attendee":
        add_col, del_col, _, _ = st.columns([3, 3, 1, 5])
        if add_col.checkbox("New attendee", False):
            my_attendees.new_attendee()
        elif del_col.checkbox("Delete an attendee", False):
            my_attendees.delete_attendee()
        # elif up_col.checkbox("Update an attendee", False):
        #    my_attendees.update_attendee()
