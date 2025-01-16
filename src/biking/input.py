from datetime import timedelta

import json

from .conversions import meters2feet, meters2miles, mps2mph, ymd2date
from .geoloc import get_elevation
from .strava import get_activities


def approx_equal(a, b, delta=1e-8):
    return abs(a - b) < delta


class InputData:
    def __init__(self, params):
        file = params.journal_file
        self.manual_data = self.load_json_file(file)
        self.date_range = self.manual_data_date_range(self.manual_data)
        self.params = params

    def load_json_file(self, file):
        with open(file) as fh:
            data = json.load(fh)

        return data

    def manual_data_date_range(self, data):
        if not data:
            return None

        manual_dates = sorted(data.keys())
        date_range = [
            ymd2date(manual_dates[0]),
            ymd2date(manual_dates[-1]),
        ]

        return date_range

    def calculate_elevation(self, activity):
        elevation = None

        lat, lng = activity["start_latlng"]
        if self.params.obscured_std_start_latlng and self.params.std_start_elevation_ft is not None:
            std_start_lat, std_start_lng = self.params.obscured_std_start_latlng
            if approx_equal(lat, std_start_lat) and approx_equal(lng, std_start_lng):
                elevation = self.params.std_start_elevation_ft

        if elevation is None:
            cache_name = self.params.cache_name
            elevation_meters = get_elevation(cache_name, lat, lng)
            elevation = meters2feet(elevation_meters)

        return elevation

    def get_strava_data(self):
        data = {}

        activities = get_activities()
        for activity in activities:
            ymd = activity["start_date_local"][:10]

            elevation = self.calculate_elevation(activity)

            record = dict(
                ymd=ymd,
                distance=meters2miles(activity["distance"]),
                total_elevation_gain=meters2feet(activity["total_elevation_gain"]),
                average_speed=mps2mph(activity["average_speed"]),
                max_speed=mps2mph(activity["max_speed"]),
                elev_high=meters2feet(activity["elev_high"]),
                elev_low=meters2feet(activity["elev_low"]),
                elev_start=elevation,
            )
            data[ymd] = record

            dt = ymd2date(ymd)
            if not self.date_range:
                self.date_range = [dt, dt]
            elif dt < self.date_range[0]:
                self.date_range[0] = dt
            elif dt > self.date_range[1]:
                self.date_range[1] = dt

        return data

    def get_normalized_strava_data(self):
        strava_data = self.get_strava_data()
        if not strava_data:
            return []

        daily_data = []
        cur_date = self.date_range[0]
        while cur_date <= self.date_range[1]:
            ymd = cur_date.strftime("%Y-%m-%d")

            if ymd in strava_data:
                record = strava_data[ymd]
            else:
                record = dict(
                    ymd=ymd,
                    distance=0,
                    total_elevation_gain=0,
                    average_speed=0,
                    max_speed=0,
                    elev_high=0,
                    elev_low=0,
                    elev_start=None,
                )
            daily_data.append(record)

            cur_date += timedelta(days=1)

        return daily_data

    def apply_manual_record(self, record, manual_record):
        record["distance"] += manual_record.get("distance", 0)
        record["total_elevation_gain"] += manual_record.get("total_elevation_gain", 0)

        if "start_latlng" in manual_record:
            cache_name = self.params.cache_name
            elevation = get_elevation(cache_name, *manual_record["start_latlng"])
            record["elev_start"] = meters2feet(elevation)

    def add_manual_data(self, daily_data):
        for record in daily_data:
            ymd = record["ymd"]
            if ymd in self.manual_data:
                manual_record = self.manual_data[ymd]
                self.apply_manual_record(record, manual_record)

    def get_daily_data(self):
        daily_data = self.get_normalized_strava_data()
        self.add_manual_data(daily_data)

        return daily_data

    def summarize(self):
        print("date        miles  elevation  speed")
        print("----------  -----  ---------  -----")
        for rec in self.get_daily_data():
            if rec['distance']:
                print(f"{rec['ymd']}  {rec['distance']:5.1f}    {rec['total_elevation_gain']:5.0f}    {rec['average_speed']:5.1f}")
            else:
                print(rec['ymd'])
