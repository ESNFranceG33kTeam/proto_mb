"""
#############################################
#
# cookies.py
#
# cookie object
#
#############################################
"""
import os
from typing import List


class Cookie:
    """Cookie params."""

    current_dir = os.path.dirname(os.path.abspath(__file__))

    HASH_COOKIES_FILE: str = (
        "{}/{}/".format(current_dir, "../resources") + ".hash_cookies.txt"
    )
    COOKIE_PREFIX: str = "mb/gosmo/"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all Cookie params."""
        return [
            Cookie.HASH_COOKIES_FILE,
            Cookie.COOKIE_PREFIX,
        ]
