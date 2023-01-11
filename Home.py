"""
#############################################
#
# Home.py
#
# Launcher
#
#############################################
"""
import time
import streamlit as st
from styles import css
from helpers import Configuration
from system import getuserlog, Health, Session


st.set_page_config(
    page_title="Module bénévole",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Welcome to the Module 2.0 ! 👋")
    st.write(
        f"Connected as `{getuserlog().username}`, with role `{getuserlog().role}`."
    )

    myconf = Configuration()

    if st.button("Log out"):
        Session.remove_from_local_storage(Session.SESSION_PREFIX)
        getuserlog().session = None
        st.session_state["password_correct"] = False
        time.sleep(1)
        st.experimental_rerun()

    st.markdown("---")
    Health().alive()
