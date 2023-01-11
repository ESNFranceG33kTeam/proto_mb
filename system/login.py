"""
#############################################
#
# login.py
#
# login object
#
#############################################
"""
import json
import random
import streamlit as st
from .cas import cas_login
from .sessions import Session
from helpers import Configuration
from streamlit.source_util import get_pages
from streamlit.runtime.scriptrunner import RerunData, RerunException


class Login:
    """Everything about the system object."""

    def __init__(self):
        """Init system object."""
        self.username = None
        self.role = None
        self.connexion_method = None
        self.session = None

    def check_password(self):
        """Returns `True` if the user had a correct password."""

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False

            self.session_state = st.session_state["password_correct"]
            self.username = st.session_state["username"]
            self.connexion_method = "classical"
            if st.session_state["username"] == "admin":
                self.role = "bureau"
            else:
                self.role = "member"

        def galaxy_connect():
            """Galaxy CAS."""
            gal_username = st.session_state["gal_username"]
            gal_password = st.session_state["gal_password"]

            if len(gal_username) > 0 and len(gal_password) > 0:
                account = cas_login(
                    service=Configuration().website,
                    username=gal_username,
                    password=gal_password,
                )
                info_account = account.get("https://accounts.esn.org/user").text
                if Configuration().galaxy in info_account:
                    del st.session_state["gal_password"]
                    self.username = gal_username
                    self.connexion_method = "galaxy"
                    st.session_state["password_correct"] = True
                    if "Regular Board Member" in info_account:
                        self.role = "bureau"
                    else:
                        self.role = "member"
                elif "Webmaster" in info_account and "ESN France" in info_account:
                    del st.session_state["gal_password"]
                    self.username = gal_username
                    self.role = "bureau"
                    self.connexion_method = "galaxy"
                    st.session_state["password_correct"] = True
                else:
                    st.error("😕 User not known or password incorrect")

        def classical_login():
            """User/Password system."""
            st.markdown("#### Classical system")
            st.text_input("Username", on_change=password_entered, key="username")
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password"
            )

        def sso_login():
            """Connect with sso."""
            st.markdown("#### Galaxy system")
            st.text_input(
                "Username or email address",
                on_change=galaxy_connect,
                key="gal_username",
            )
            st.text_input(
                "Password",
                type="password",
                on_change=galaxy_connect,
                key="gal_password",
            )

        if "password_correct" not in st.session_state:
            # First run, show inputs for username + password.
            classical_login()
            sso_login()
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            classical_login()
            sso_login()
            if len(st.session_state["password"]) > 0:
                st.error("😕 User not known or password incorrect")
            return False
        else:
            # Connexion is ok.
            if self.session is None:
                token = hash((self.username, self.role, random.randint(0, 10000)))
                self.session = {
                    "session-mb": {
                        f"{Session.SESSION_PREFIX}username": f"{self.username}",
                        f"{Session.SESSION_PREFIX}role": f"{self.role}",
                        f"{Session.SESSION_PREFIX}connexion_method": f"{self.connexion_method}",
                        f"{Session.SESSION_PREFIX}token": f"{token}",
                    }
                }

                Session.set_to_local_storage(Session.SESSION_PREFIX, self.session)

                with open(Session.HASH_SESSIONS_FILE, "a") as sessions_file:
                    sessions_file.write(str(hash(json.dumps(self.session))) + "\n")
            return True

    @staticmethod
    def switch_page(page_name: str):
        """Switch page

        Args:
            page_name: name of the page to target
        """
        page_name = page_name.lower().replace("_", " ")
        pages = get_pages("streamlit_app.py")

        for page_hash, config in pages.items():
            if config["page_name"].lower().replace("_", " ") == page_name:
                raise RerunException(
                    RerunData(
                        page_script_hash=page_hash,
                        page_name=page_name,
                    )
                )

    def check_perm(self, role_need: str):
        """Check role to access page.

        Args:
            role_need: the minimal role need.
        """
        if self.role != role_need:
            self.switch_page("Home")

    def load_session(self):
        """Load session."""
        _session = Session.get_from_local_storage(Session.SESSION_PREFIX)
        with open(Session.HASH_SESSIONS_FILE, "r") as sessions_file:
            content = sessions_file.read()

            if str(hash(json.dumps(_session))) in content:
                self.username = _session["session-mb"][
                    f"{Session.SESSION_PREFIX}username"
                ]
                self.role = _session["session-mb"][f"{Session.SESSION_PREFIX}role"]
                self.connexion_method = _session["session-mb"][
                    f"{Session.SESSION_PREFIX}connexion_method"
                ]
                st.session_state["password_correct"] = True
                self.session = _session
            else:
                self.session = None


userlog = Login()


def getuserlog():
    """Return the log user."""
    if "password_correct" not in st.session_state:
        userlog.load_session()
    return userlog
