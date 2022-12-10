"""
#############################################
#
# 9_Check.py
#
# health check page
#
#############################################
"""
import streamlit as st
from system import getuserlog, Health
from helpers import Configuration
from styles import css


st.set_page_config(
    page_title="Check",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():
    getuserlog().check_perm("bureau")

    def profile():
        """Profile function."""
        st.markdown("### Association Profile")
        myconf = Configuration()
        st.json(vars(myconf), expanded=False)

    st.write("# Check page ! ⚙️")

    Health().alive()
    Health().status()
    profile()
