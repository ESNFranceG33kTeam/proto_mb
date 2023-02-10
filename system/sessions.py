"""
#############################################
#
# sessions.py
#
# session object
#
#############################################
"""
import os
import json
from typing import List
from streamlit_javascript import st_javascript


class Session:
    """Session params."""

    current_dir = os.path.dirname(os.path.abspath(__file__))

    HASH_SESSIONS_FILE: str = (
        "{}/{}/".format(current_dir, "../resources") + ".hash_sessions.txt"
    )
    SESSION_PREFIX: str = "mb/gosmo/"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all Session params."""
        return [
            Session.HASH_SESSIONS_FILE,
            Session.SESSION_PREFIX,
        ]

    @staticmethod
    def get_from_local_storage(key) -> json:
        """Get local storage data.

        Args:
            key: id of the data
        Return:
            json
        """
        data = st_javascript(f"JSON.parse(localStorage.getItem('{key}'));")
        return data or {}

    @staticmethod
    def set_to_local_storage(key, data):
        """Register data into local storage.

        Args:
            key: id for the data
            data: the data in json format
        """
        st_javascript(f"localStorage.setItem('{key}', JSON.stringify({data}));")

    @staticmethod
    def remove_from_local_storage(key):
        """Remove data from local storage.

        Args:
            key: id of the data to remove
        """
        st_javascript(f"localStorage.removeItem('{key}');")
