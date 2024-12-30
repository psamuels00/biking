#!/usr/bin/env python

import json

from biking.strava import build_strava


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
