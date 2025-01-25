import os
import sys



def attributes(name, **values):
    return type(name, (object,), values)()


class Parameters:
    def __init__(self):
        self.http_cache_name = ".cache_strava"
        self.http_cache_expire_sec = 24 * 3600
        self.access_tokens_file = ".access_tokens"
        self.strava_client_id = self.load("strava_client_id")
        self.strava_client_secret = self.load("strava_client_secret")
        self.strava_app_auth_code = self.load("strava_app_auth_code")
        self.url = attributes("UrlParams",
            token="https://www.strava.com/oauth/token",
            athlete="https://www.strava.com/api/v3/athlete",
            activities="https://www.strava.com/api/v3/athlete/activities",
        )

    @staticmethod
    def load(name):
        value = os.getenv(name)
        if not value:
            print(f"Error: environment variable '{name}' not set or empty.", file=sys.stderr)
            sys.exit(1)

        return value
