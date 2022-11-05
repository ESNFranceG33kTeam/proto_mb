import streamlit as st
from call import Call


def info():
    page_name = "Adherents"
    endpoint = "auth/adherents"
    protocol = "post"
    return page_name, endpoint, protocol


def app():
    endpoint = "auth/adherents"

    st.write("## New Adherent !")

    post_new = Call()

    #post_new.post_url(endpoint=endpoint)

    if post_new.status_code != 200:
        st.warning(post_new.response)
