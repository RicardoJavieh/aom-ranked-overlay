import requests

from config import AOMSTATS_PROFILES_URL, HEADERS, FLAG_ICON_URL

class Player:

    def __init__(self, alias):

        self.alias = alias
        self.countryCode = ""
        self.countrySVGFlag = ""
        self.clan_name = ""
        self.sup_team_rank = 0
        self.sup_team_rating = 0

    def fetchFlag(self):

        if not self.countryCode:
            return

        response = requests.get(
            FLAG_ICON_URL.format(
                country=self.countryCode.lower()
            ),
            headers=HEADERS,
            timeout=5
        )

        response.raise_for_status()
        self.countrySVGFlag = response.text

    def fetch(self):

        response = requests.get(
            AOMSTATS_PROFILES_URL,
            params={"s": self.alias},
            headers=HEADERS,
            timeout=5
        )

        response.raise_for_status()
        data = response.json()
        exact = next(
            (
                p for p in data.get("profiles", [])
                if p.get("alias", "").lower() == self.alias.lower()
            ),
            None
        )

        if not exact:
            raise Exception(f"Player not found: {self.alias}")

        self.countryCode = exact.get("country", "")
        self.clan_name = exact.get("clan_name", "")
        self.sup_team_rank = exact.get("sup_team_rank", 0)
        self.sup_team_rating = exact.get("sup_team_rating", 0)

        self.fetchFlag()