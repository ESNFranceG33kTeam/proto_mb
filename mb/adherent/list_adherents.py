import streamlit as st
from mb.call import Call


def info():
    page_name = "Adherents"
    endpoint = "auth/adherents"
    return page_name, endpoint


def app():
    endpoint = "auth/adherents"

    get_list = Call()

    get_list.get_url(endpoint=endpoint)

    if get_list.status_code != 200:
        st.warning()
