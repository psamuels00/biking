from .auth import Authentication
from .credentials import Credentials
from .request import Request


class Strava:
    def __init__(self, params):
        credentials = Credentials(params)
        auth = Authentication(params, credentials)
        self.request = Request(params, auth)

    def get_athlete(self):
        return self.request.get_athlete()

    def get_activities(self):
        return self.request.get_activities()

    def get_new_activities(self, cached_activities):
        return self.request.get_new_activities(cached_activities)
