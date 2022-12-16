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
from .cookies import Cookie
from helpers import Configuration
import extra_streamlit_components as stx
from streamlit.source_util import get_pages
from streamlit.runtime.scriptrunner import RerunData, RerunException


class Login:
    """Everything about the system object."""

    def __init__(self):
        """Init system object."""
        self.username = None
        self.role = None
        self.connexion_method = None
        self.cookie_manager = None
        self.cookies = None

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
            if self.cookies is None:
                token = hash((self.username, self.role, random.randint(0, 10000)))
                self.cookies = {
                    "cookies-mb": {
                        f"{Cookie.COOKIE_PREFIX}username": f"{self.username}",
                        f"{Cookie.COOKIE_PREFIX}role": f"{self.role}",
                        f"{Cookie.COOKIE_PREFIX}connexion_method": f"{self.connexion_method}",
                        f"{Cookie.COOKIE_PREFIX}token": f"{token}",
                    }
                }
                self.cookie_manager.set(
                    cookie=Cookie.COOKIE_PREFIX,
                    val=self.cookies,
                    key="create_cookies",
                )

                with open(Cookie.HASH_COOKIES_FILE, "a") as cookies_file:
                    cookies_file.write(str(hash(json.dumps(self.cookies))) + "\n")
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

        _cookies = self.cookie_manager.get(cookie=Cookie.COOKIE_PREFIX)
        with open(Cookie.HASH_COOKIES_FILE, "r") as cookies_file:
            content = cookies_file.read()

            if str(hash(json.dumps(_cookies))) in content:
                self.username = _cookies["cookies-mb"][
                    f"{Cookie.COOKIE_PREFIX}username"
                ]
                self.role = _cookies["cookies-mb"][f"{Cookie.COOKIE_PREFIX}role"]
                self.connexion_method = _cookies["cookies-mb"][
                    f"{Cookie.COOKIE_PREFIX}connexion_method"
                ]
                # _token = _cookies["cookies-mb"][f"{self.cookie_prefix}token"]
                st.session_state["password_correct"] = True
                self.cookies = _cookies
            else:
                self.cookies = None


userlog = Login()


def getuserlog():
    """Return the log user."""
    if "password_correct" not in st.session_state:
        userlog.load_cookies()
    return userlog
