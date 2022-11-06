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
from call import Call


def alive():
    a_live = Call()
    a_live.req_url(endpoint="health", protocol="get")

    if a_live.status_code != 200:
        st.error("The CosmoAppy doesn't respond.")
    else:
        st.success("The CosmoAppy is ready.")
        st.json(a_live.response)


st.set_page_config(
    page_title="Check",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)

st.write("# Check page ! ⚙️")

alive()
