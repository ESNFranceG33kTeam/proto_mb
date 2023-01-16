"""
#############################################
#
# helpers.py
#
# Conf file
#
#############################################
"""
import os
import yaml
from yaml.loader import SafeLoader


class Configuration:
    """Configuration class."""

    def __init__(self):
        """Init Configuration object."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        conf_folder = "../conf"
        with open("{}/{}/".format(current_dir, conf_folder) + "conf.yaml") as f:
            data = yaml.load(f, Loader=SafeLoader)
        res_folder = "../resources"
        with open("{}/{}/".format(current_dir, res_folder) + "countries.yaml") as f:
            country = yaml.load(f, Loader=SafeLoader)

        # Association info
        self.asso_name = data["association"]["name"]
        self.asso_id = data["association"]["id"]
        self.adhesion_price = data["association"]["adhesion_price"]
        self.address_city = data["association"]["address"]["city"]
        self.address_postalcode = data["association"]["address"]["postal_code"]
        self.address_street = data["association"]["address"]["street"]
        self.address_extra = data["association"]["address"]["extra"]
        self.website = data["association"]["website"]
        self.galaxy = data["association"]["galaxy"]
        self.facebook = data["association"]["facebook"]
        self.email = data["association"]["email"]
        # More info
        self.adh_situation = data["adherent"]["situation"]
        self.esncard_price = data["esncard_price"]
        self.universities = data["universities"]
        self.event_types = data["event_types"]
        self.lang = data["lang"]
        # API info
        self.api_prefix = data["api"]["prefix"]
        self.api_dns = data["api"]["url"]
        self.api_port = data["api"]["port"]
        self.api_token = data["api"]["token"]

        # Country list
        self.countries = country["countries"]
