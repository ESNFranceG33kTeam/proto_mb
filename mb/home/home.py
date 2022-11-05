import streamlit as st


def info():
    page_name = "home"
    return page_name


def app():
    home_page = """
    <div align="center">
        Welcome in the Mb 2.0 !
    </div>
    </br>
    """
    st.markdown(home_page, unsafe_allow_html=True)
