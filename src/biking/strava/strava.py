from requests_cache import CachedSession

from .auth import Authentication
from .credentials import Credentials
from .params import Parameters


class StravaBase:
    def __init__(self, params, auth):
        self.auth = auth

        name = params.http_cache_name
        expire_sec = params.http_cache_expire_sec
        self.session = CachedSession(name, expire_after=expire_sec)

    def fetch(self, url, params=None, level=0):
        access_token = self.auth.credentials.access_token
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        args = dict()
        if params:
            args["params"] = params

        response = self.session.get(url, headers=headers, **args)

        # if response.from_cache:
        #     print("@@@ Response was served from cache.")
        # else:
        #     print("@@@ Fetched a fresh response.")

        data = response.json()

        token_expired = (
                response.status_code == 401
                and data["message"] == "Authorization Error"
                and data["errors"][0]["field"] == "access_token"
                and data["errors"][0]["code"] == "invalid"
        )

        if response.status_code == 200:
            # print(json.dumps(data, indent=4))
            return data
        elif not token_expired or level > 1:
            print(f"**** Error: {response.status_code}")
            print("**** Response:", response.text)
            return None

        self.auth.refresh_tokens()
        return self.fetch(url, params, level + 1)


class Strava(StravaBase):
    def get_athlete(self):
        url = "https://www.strava.com/api/v3/athlete"
        data = self.fetch(url)

        return data

    def get_activities(self):
        url = "https://www.strava.com/api/v3/athlete/activities"
        params = dict(
            per_page=100,
            page=1,
        )
        data = self.fetch(url, params)

        return data


def build_strava():
    parameters = Parameters()
    credentials = Credentials(parameters)
    auth = Authentication(credentials)
    strava = Strava(parameters, auth)

    return strava
