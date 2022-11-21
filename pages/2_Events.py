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
from controllers.event import Event
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

    PAGES = {
        "List": [my_events.list_events, my_events.update_event],
        "New": [my_events.new_event],
    }
    selection = st.sidebar.radio(
        "Navigation event", list(PAGES.keys()), label_visibility="hidden"
    )

    if my_events.json_pd is None:
        st.warning("Data is empty !")
    else:
        for page in PAGES[selection]:
            page()
            st.markdown("---")
