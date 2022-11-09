"""
#############################################
#
# login.py
#
# login object
#
#############################################
"""
import streamlit as st
import extra_streamlit_components as stx
from streamlit.source_util import get_pages
from streamlit.runtime.scriptrunner import RerunData, RerunException


class Login:
    """Everything about the system object."""

    def __init__(self):
        """Init system object."""
        self.username = ""
        self.role = ""
        self.connexion_method = ""
        self.session_state = False
        self.cookie_manager = None
        self.cookies = None
        self.cookie_prefix = "mb/gosmo/"

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
            if "load_state" not in st.session_state:
                st.session_state.load_state = False

            def galaxy_connect():
                """Galaxy CAS."""
                # Get return from galaxy:
                # self.username = galaxy.pseudo
                # self.role = galaxy.role
                self.username = "galaxy"
                self.role = "bureau"
                self.connexion_method = "galaxy"
                st.session_state["password_correct"] = True
                self.session_state = st.session_state["password_correct"]

            if st.checkbox("Galaxy"):
                galaxy_connect()
                self.switch_page("Home")

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
            self.cookie_manager.set(
                cookie=self.cookie_prefix + "username",
                val=self.username,
                key="set_username",
            )
            self.cookie_manager.set(
                cookie=self.cookie_prefix + "role", val=self.role, key="set_role"
            )
            self.cookies = {
                "cookies-mb": {
                    f"{self.cookie_prefix}username": f"{self.username}",
                    f"{self.cookie_prefix}role": f"{self.role}",
                }
            }
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

    def load_cookies(self):
        """Load cookies."""
        self.cookie_manager = stx.CookieManager()

        val_username = self.cookie_manager.get(cookie=self.cookie_prefix + "username")
        val_role = self.cookie_manager.get(cookie=self.cookie_prefix + "role")

        if val_username is not None and val_role is not None:
            self.username = val_username
            self.role = val_role
            st.session_state["password_correct"] = True
            self.session_state = st.session_state["password_correct"]
            self.cookies = {
                "cookies-mb": {
                    f"{self.cookie_prefix}username": "{self.username}",
                    f"{self.cookie_prefix}role": "{self.role}",
                }
            }


userlog = Login()


def getuserlog():
    """Return the log user."""
    if "password_correct" not in st.session_state:
        userlog.load_cookies()
    return userlog
