#!/usr/bin/env python

import json
import os
import requests
import sys

from requests_cache import CachedSession


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


class Credentials:
    def __init__(self, parameters):
        self.parameters = parameters

        self.client_id = parameters.strava_client_id
        self.client_secret = parameters.strava_client_secret
        self.app_auth_code = parameters.strava_app_auth_code

        self.access_token = None
        self.refresh_token = None

    def load_access_tokens(self):
        file = self.parameters.access_tokens_file
        if not os.path.exists(file):
            return False

        self.access_token = None
        self.refresh_token = None

        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    name, value = line.split("=", 1)
                    if name == "access_token":
                        self.access_token = value
                    elif name == "refresh_token":
                        self.refresh_token = value

        return self.access_token and self.refresh_token

    def store_access_tokens(self):
        file = self.parameters.access_tokens_file

        with open(file, "w") as f:
            f.write(f"access_token={self.access_token}\n")
            f.write(f"refresh_token={self.refresh_token}\n")


class Authentication:
    def __init__(self, credentials):
        self.credentials = credentials

        if not credentials.load_access_tokens():
            self.exchange_tokens()

    def exchange_tokens(self, refresh=False):
        url = "https://www.strava.com/oauth/token"

        data = dict(
            client_id=self.credentials.client_id,
            client_secret=self.credentials.client_secret,
        )

        if not refresh:
            data["code"] = self.credentials.app_auth_code
            data["grant_type"] = "authorization_code"
        else:
            data["refresh_token"] = self.credentials.refresh_token
            data["grant_type"] = "refresh_token"

        response = requests.post(url, data=data)

        if response.status_code == 200:
            data = response.json()

            self.credentials.access_token = data["access_token"]
            self.credentials.refresh_token = data["refresh_token"]
            self.credentials.store_access_tokens()
        else:
            print(f"**** Error: {response.status_code}")
            print("**** Response:", response.text)

    def refresh_tokens(self):
        self.exchange_tokens(refresh=True)


class Strava:
    def __init__(self, params, auth):
        self.auth = auth

        name = params.http_cache_name
        expire_sec = params.http_cache_expire_sec
        self.session = CachedSession(name, expire_after=expire_sec)

    def cached_get(self, url, params=None, level=0):
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
            #print(json.dumps(data, indent=4))
            return data
        elif not token_expired or level > 1:
            print(f"**** Error: {response.status_code}")
            print("**** Response:", response.text)
            return None

        self.auth.refresh_tokens()
        return self.cached_get(url, params, level + 1)

    def get_athlete(self):
        url = "https://www.strava.com/api/v3/athlete"
        data = self.cached_get(url)

        return data

    def get_activities(self):
        url = "https://www.strava.com/api/v3/athlete/activities"
        params = dict(
            per_page=100,
            page=1,
        )
        data = self.cached_get(url, params)

        return data


def build_strava():
    parameters = Parameters()
    credentials = Credentials(parameters)
    auth = Authentication(credentials)
    strava = Strava(parameters, auth)

    return strava


def get_activities():
    strava = build_strava()
    return strava.get_activities()


def main():
    strava = build_strava()

    data = strava.get_athlete()
    print("Athlete:")
    print(json.dumps(data, indent=4))

    data = strava.get_activities()
    print("Activities:")
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
