"""
#############################################
#
# 1_Events.py
#
# Events page
#
#############################################
"""
import streamlit as st
from controllers.event import Event, Attendee
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Event",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Events")

    my_events = Event()
    my_events.get_data()
    my_attendees = Attendee()
    my_attendees.get_data()

    PAGES = {
        "List": [my_events.list_events, my_events.update_event],
        "New": [my_events.new_event],
        "Attendee": [my_attendees.list_attendees],
    }
    selection = st.sidebar.radio(
        "Navigation event", list(PAGES.keys()), label_visibility="hidden"
    )

    if my_events.json_pd is None:
        st.warning("Data is empty !")

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
