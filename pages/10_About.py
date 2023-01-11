"""
#############################################
#
# 10_About.py
#
# about page
#
#############################################
"""
import streamlit as st
from helpers import Configuration
from styles import css


st.set_page_config(
    page_title="About",
    page_icon=":busts_in_silhouette:",
    layout="wide",
    initial_sidebar_state="auto",
)
css()

myconf = Configuration()

st.write("# About️")

# About the association
st.markdown(f"## {myconf.asso_name}")
st.markdown(
    f"""
{myconf.asso_name} is a not lucrative None Governmental Organisation and its part of ESN
international.

The ESN network works with other associations in the area to promote the reception of young
people and jointly carry out reception projects.

The association is based at :
{myconf.address_street} {myconf.address_extra} {myconf.address_postalcode} {myconf.address_city}.

Association website : {myconf.website}

Association email : {myconf.email}
    """,
    unsafe_allow_html=True,
)

# Terms and conditions
st.markdown("## Terms and conditions")
st.markdown(
    f"""
##### Status :

- Being an adherent :
    - I accept {myconf.asso_name} to stock my personal information for 365 days.
    - As an adherent, I'm able to participated to any event of the association.
<br/>

- Being a volunteer :
    - A volunteer have to be an actual adherent and have his adhesion always up to date in order \
to stay a volunteer.
    - I accept {myconf.asso_name} to stock my personal information for the duration of my \
engagement.
    - As a volunteer, I'm able to participated to any event of the association.
    - As a volunteer, i'm able to organized any event of the association.
<br/>

- Being an alumni :
    - I accept {myconf.asso_name} to stock my personal information for further alumni event.
<br/>

##### Events :
- In order to participated any event, the people have to be an adherent.
- In case of cancellation of an event, the association gonna refund every adherent.
- In case of spot cancellation from an adherent, the association keep to right to study the \
case in order to refund or not the adherent.
    """,
    unsafe_allow_html=True,
)

# Data keeping
st.markdown("## Data politic")
st.markdown(
    """
Follow the GDPR and the French law :

- We keep data about our adherent only during 365 days following the adhesion, \
after that the adherent and his data gonna be delete.
- If the adhesion is updated before the end of the 365 days, the adherent and his data gonna be \
keep for 365 days following the day of the update.
<br/>

- For the volunteers :
    - We keep the personal information for the duration of the engagement.
<br/>

- For the alumni :
    - We keep the personal information for further alumni event \
if and only if the volunteer is right to become an alumni.
    - If not, the volunteer is not becoming an alumni and his personal information are delete.
<br/>

- For our archives, we keep general data as:
    - Number of adherents per year
    - Number of volunteers
    - Number of alumni
    - Number of participation in our events
    - Number of adherent in each university
    - Number of adherent from each country
We don't keep personal data of our adherent and don't link one data to another.
    """,
    unsafe_allow_html=True,
)
