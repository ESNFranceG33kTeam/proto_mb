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


st.set_page_config(
    page_title="Module bénévole",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

st.write("# Welcome to the Module 2.0 ! 👋")

myconf = Configuration()
