from .strava import build_strava


def get_activities():
    strava = build_strava()
    return strava.get_activities()
