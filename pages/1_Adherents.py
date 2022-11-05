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
from adherent import list_adherents
from adherent import new_adherent


st.set_page_config(
    page_title="Check",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)

st.write("# Adherents")

PAGES = {
    "List": list_adherents,
    "New": new_adherent
}

selection = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility='hidden')

page = PAGES[selection]
page.app()
