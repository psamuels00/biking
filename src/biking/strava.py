#!/usr/bin/env python

import json

from strava.auth import Authentication
from strava.credentials import Credentials
from strava.params import Parameters
from strava.strava import Strava


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
