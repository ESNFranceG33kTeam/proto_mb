"""
#############################################
#
# 8_Bureau.py
#
# Bureau page
#
#############################################
"""
import streamlit as st
from controllers.money import Money
from system import getuserlog
from styles import css


st.set_page_config(
    page_title="Bureau",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

if getuserlog().check_password():
    getuserlog().check_perm("bureau")

    st.write("# Money operations")

    my_moneys = Money()
    my_moneys.get_data()

    PAGES = {
        "Money": [my_moneys.list_moneys, my_moneys.new_money],
    }
    selection = st.sidebar.radio(
        "Navigation money", list(PAGES.keys()), label_visibility="hidden"
    )

    if my_moneys.json_pd is None:
        st.warning("Data is empty !")
    else:
        for page in PAGES[selection]:
            page()
            st.markdown("---")
