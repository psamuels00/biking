#!/usr/bin/env python

import json

from biking.params import Parameters
from biking.strava import Strava


def main():
    params = Parameters()
    strava = Strava(params.strava)

    data = strava.get_athlete()
    print("Athlete:")
    print(json.dumps(data, indent=4))

    data = strava.get_activities()
    print("Activities:")
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
