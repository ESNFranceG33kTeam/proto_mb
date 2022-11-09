"""
#############################################
#
# 0_My_account.py
#
# profile page
#
#############################################
"""
import streamlit as st
from system import getuserlog

st.set_page_config(
    page_title="My account",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)

if getuserlog().check_password():

    def profile():
        """My account function."""
        st.markdown("### My account")
        myaccount = getuserlog()
        st.json(vars(myaccount))

    st.write("# Account ! ⚙️")

    profile()
