"""
#############################################
#
# common.py
#
# common design function
#
#############################################
"""
import streamlit as st


def css():
    """Function to add header footer and hide streamlit menu."""
    # To hide the menu : `visibility: hidden`
    hea_foo = """
        <style>
            MainMenu {visibility: visible;}
            footer::before {content:'Module bénévole | G33kTeam™️ | Since 2023 | ';}
        </style>
    """
    st.markdown(hea_foo, unsafe_allow_html=True)
