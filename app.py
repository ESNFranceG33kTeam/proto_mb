"""
#############################################
#
# app.py
#
# Launcher
#
#############################################
"""
import streamlit as st
from mb import common
from mb import health
from mb import home

# from mb import adherent
# from mb import planning
# from mb import event
# from mb import money
# from mb import stocks
# from mb import stats

st.set_page_config(
    page_title="Module bénévole",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
common.css()
common.menu()

PAGES = {
    "Home": home,
    "Check": health
}
selection = st.sidebar.radio("Navigation", list(PAGES.keys()))

#####################################################################
# Start check

#####################################################################
# Change page
page = PAGES[selection]
page.app()
