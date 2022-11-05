import streamlit as st
import pandas as pd
import json

from call import Call


def info():
    page_name = "Adherents"
    endpoint = "auth/adherents"
    protocol = "get"
    return page_name, endpoint, protocol


def app():
    st.write("## List of Adherents !")

    get_list = Call()

    get_list.get_url(endpoint="auth/adherents")

    if get_list.status_code != 200:
        st.warning(get_list.response)

    for adh in get_list.response:
        del adh["created_at"]
        del adh["updated_at"]

    json_dec = json.dumps(get_list.response)
    json_pd = pd.read_json(json_dec)
    json_pd.set_index('id', inplace=True)

    # List data
    s_filter = st.checkbox("Search filters", False)

    if s_filter:
        selected_name = st.selectbox('Select firstname or lastname :', json_pd["firstname"])
        selected_rows = json_pd.loc[(json_pd['firstname'] == selected_name) | (json_pd['lastname'] == selected_name)]
        data_adh = selected_rows
    else:
        data_adh = json_pd

    st.write(data_adh)

    st.write("## Update an Adherent")
    st.markdown("If you want to auto complete most of the item, selected the `id` of the adherent.")

    # Update data
    selected_indices = st.selectbox('Select rows:', json_pd.index)
    with st.form("Update", clear_on_submit=False):
        id_adh = st.text_area("id", selected_indices)
        firstname_adh = st.text_area("Firstname", json_pd.loc[selected_indices, "firstname"])
        lastname_adh = st.text_area("Lastname", json_pd.loc[selected_indices, "lastname"])
        email_adh = st.text_area("Email", json_pd.loc[selected_indices, "email"])
        dateofbirth_adh = st.text_area("Date of birth", json_pd.loc[selected_indices, "dateofbirth"])
        student_adh = st.checkbox("Student ?", json_pd.loc[selected_indices, "student"])
        university_adh = st.text_area("University", json_pd.loc[selected_indices, "university"])
        homeland_adh = st.text_area("Homeland", json_pd.loc[selected_indices, "homeland"])
        speakabout_adh = st.text_area("How does he learn about us ?", json_pd.loc[selected_indices, "speakabout"])
        newsletter_adh = st.checkbox("Newsletter ?", json_pd.loc[selected_indices, "newsletter"])

        submitted = st.form_submit_button("Submit")
        if submitted:
            if len(id_adh) > 0 and len(firstname_adh) > 0:
                # make a put_curl
                st.write("Adherent updated ✌️")
            else:
                st.write("You forget some info...")
