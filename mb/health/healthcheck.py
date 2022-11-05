"""
#############################################
#
# healthcheck.py
#
# health check test
#
#############################################
"""
import streamlit as st
from mb.call import Call


def info():
    page_name = "Check"
    endpoint = "health"
    return page_name, endpoint


def alive():
    a_live = Call()
    a_live.get_url(endpoint="health")

    if a_live.status_code != 200:
        st.error("The CosmoAppy doesn't respond.")
    else:
        st.success("The CosmoAppy is ready.")
        st.json(a_live.response)


def app():
    alive()
