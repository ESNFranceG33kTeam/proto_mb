"""
#############################################
#
# 1_Adherents.py
#
# Adherents page
#
#############################################
"""
import streamlit as st
from controllers.adherent import Adherent
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Adherent",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():

    st.write("# Adherents")

    my_adherents = Adherent()

    PAGES = {
        "List": [
            my_adherents.list_adherents,
            my_adherents.update_adherent,
            my_adherents.renew_adherent,
        ],
        "New": [my_adherents.new_adherent],
    }
    selection = st.sidebar.radio(
        "Navigation adherent", list(PAGES.keys()), label_visibility="hidden"
    )

    for page in PAGES[selection]:
        page()
        st.markdown("---")
