"""
#############################################
#
# Home.py
#
# Launcher
#
#############################################
"""
import streamlit as st
from styles import css
from helpers import Configuration
from system import getuserlog, Health, Cookie


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
        _cookies = getuserlog().cookie_manager.get(
            cookie=Cookie.COOKIE_PREFIX
        )
        if _cookies is not None:
            getuserlog().cookie_manager.delete(
                Cookie.COOKIE_PREFIX, key="delete_cookies"
            )
        getuserlog().cookies = None
        st.session_state["password_correct"] = False

    st.markdown("---")
    Health().alive()
