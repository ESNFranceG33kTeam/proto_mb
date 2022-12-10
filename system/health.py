"""
#############################################
#
# health.py
#
# object for api healthcheck
#
#############################################
"""
import streamlit as st
from .call import Call


class Health:
    """Health class.
    Everything about api healthcheck object.
    """

    def __init__(self):
        """Init Health object."""
        self.call = Call()
        self.alive_endpoint = "health"
        self.status_endpoint = "auth/status"
        self.status_code = 200

    def alive(self):
        """Healthcheck function."""
        st.markdown("### Healcheck")
        a_live = self.call
        a_live.req_url(endpoint=self.alive_endpoint, protocol="get")

        if a_live.status_code != 200:
            st.error("The CosmoAppy doesn't respond.")
            self.status_code = a_live.status_code
        else:
            st.success("The CosmoAppy is ready.")
            st.json(a_live.response)

    def status(self):
        """Status function."""
        st.markdown("### Status")
        a_status = self.call
        a_status.req_url(endpoint=self.status_endpoint, protocol="get")

        if a_status.status_code != 200:
            st.error("The CosmoAppy doesn't respond.")
            self.status_code = a_status.status_code
        else:
            st.success("Everything looks fine.")
            st.json(a_status.response)
