import streamlit as st


def css():
    hea_foo = """
        <style>
            #MainMenu {visibility: hidden;}
            footer::before {content:'Module bénévole | G33kTeam™️ | Since 2023 | ';}
        </style>
    """
    st.markdown(hea_foo, unsafe_allow_html=True)


def menu():
    pass
