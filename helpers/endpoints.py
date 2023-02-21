"""
#############################################
#
# endpoints.py
#
# endpoint object
#
#############################################
"""
from typing import List


class Endpoint:
    """Endpoints list."""

    SSO: str = "accounts.esn.org"

    ADHS: str = "auth/adherents"
    VLTS: str = "auth/volunteers"
    MONS: str = "auth/moneys"
    RPTS: str = "auth/reports"

    PLAS: str = "auth/plannings"
    PLA_ATTS: str = "auth/planning_attendees"
    PLA_ATT_PLA: str = PLA_ATTS + "/id_planning"
    PLA_ATT_VLT: str = PLA_ATTS + "/id_volunteer"

    EVES: str = "auth/events"
    EVE_ATTS: str = "auth/event_attendees"
    EVE_ATT_EVE: str = EVE_ATTS + "/id_event"
    EVE_ATT_ADH: str = EVE_ATTS + "/id_adherent"
    EVE_STAS: str = "auth/event_staffs"
    EVE_STA_EVE: str = EVE_STAS + "/id_event"
    EVE_STA_VLT: str = EVE_STAS + "/id_volunteer"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all Endpoints."""
        return [
            Endpoint.SSO,
            Endpoint.ADHS,
            Endpoint.VLTS,
            Endpoint.MONS,
            Endpoint.RPTS,
            Endpoint.PLAS,
            Endpoint.PLA_ATTS,
            Endpoint.PLA_ATT_PLA,
            Endpoint.PLA_ATT_VLT,
            Endpoint.EVES,
            Endpoint.EVE_ATTS,
            Endpoint.EVE_ATT_EVE,
            Endpoint.EVE_ATT_ADH,
            Endpoint.EVE_STAS,
            Endpoint.EVE_STA_EVE,
            Endpoint.EVE_STA_VLT,
        ]
