import numpy as np

from .conversions import meters2feet
from .geoloc import get_elevation


def approx_equal(a, b, delta=1e-8):
    return abs(a - b) < delta


class Elevation:
    def __init__(self, params):
        self.params = params

    def calculate_activity_start(self, activity):
        if not activity.get("start_latlng", []):
            return np.nan

        elevation = None
        lat, lng = activity["start_latlng"]

        if self.params.obscured_std_start_latlng and self.params.std_start_elevation_ft is not None:
            std_start_lat, std_start_lng = self.params.obscured_std_start_latlng
            if approx_equal(lat, std_start_lat) and approx_equal(lng, std_start_lng):
                elevation = self.params.std_start_elevation_ft

        if elevation is None:
            cache_name = self.params.elevation_cache_name
            elevation_meters = get_elevation(cache_name, lat, lng)
            elevation = meters2feet(elevation_meters)

        return elevation