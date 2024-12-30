import os
import sys



class Parameters:
    def __init__(self):
        self.http_cache_name = ".strava_cache"
        self.http_cache_expire_sec = 24 * 3600
        self.access_tokens_file = ".access_tokens"
        self.strava_client_id = self.load("strava_client_id")
        self.strava_client_secret = self.load("strava_client_secret")
        self.strava_app_auth_code = self.load("strava_app_auth_code")

    @staticmethod
    def load(name):
        value = os.getenv(name)
        if not value:
            print(f"Error: environment variable '{name}' not set or empty.", file=sys.stderr)
            sys.exit(1)

        return value
