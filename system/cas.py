"""
#############################################
#
# cas.py
#
# cas method
#
#############################################
"""
import requests
import lxml.html


def cas_login(service: str, username: str, password: str) -> requests.session():
    """Init a cas connexion.

    Args:
        service: your service address
        username: your username for the connexion
        password: your password for the connexion
    Return:
        the request session
    """
    # GET parameters - URL we'd like to log into.
    params = {"service": service}
    cas_url = "https://accounts.esn.org/cas/login"

    # Start session and get login form.
    session = requests.session()
    login = session.get(cas_url, params=params)

    # Get the hidden elements and put them in our form.
    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_elements}

    # "Fill out" the form.
    form["username"] = username
    form["password"] = password
    form["op"] = "Submit"

    # Finally, login and return the session.
    session.post(cas_url, data=form, params=params)
    return session
