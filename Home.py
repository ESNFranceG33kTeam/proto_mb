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
from system import getuserlog, Health


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
        val_username = getuserlog().cookie_manager.get(
            cookie=getuserlog().cookie_prefix + "username"
        )
        val_role = getuserlog().cookie_manager.get(
            cookie=getuserlog().cookie_prefix + "role"
        )
        if val_username is not None:
            getuserlog().cookie_manager.delete(
                getuserlog().cookie_prefix + "username", key="delete_username"
            )
        if val_role is not None:
            getuserlog().cookie_manager.delete(
                getuserlog().cookie_prefix + "role", key="delete_role"
            )
        st.session_state["password_correct"] = False

    st.markdown("---")
    Health().alive()
