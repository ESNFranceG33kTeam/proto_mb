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
from styles import css, menu

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
css()
menu()

st.write("# Welcome to the Module 2.0 ! 👋")
