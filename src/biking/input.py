from datetime import timedelta

from .conversions import meters2feet, meters2miles, mps2mph, ymd2date
from .geoloc import get_elevation
from .strava import get_activities


def approx_equal(a, b, delta=1e-8):
    return abs(a - b) < delta


class InputData:
    # used to capture info on skipped days and rides prior to the use of Strava
    # ...or days when *someone* forgets to record a route using Strava
    manual_data = {
        "2024-10-11": {"distance": 10},
        "2024-10-12": {"distance": 6.9},
        "2024-10-13": {"distance": 9},
        "2024-10-14": {"distance": 11},
        "2024-10-15": {"distance": 11},
        "2024-10-16": {"distance": 11},
        "2024-10-17": {"distance": 13},
        "2024-10-18": {"distance": 14},
        "2024-10-19": {"distance": 23},
        "2024-10-20": {"distance": 8},
        "2024-10-21": {"distance": 10},
        "2024-10-22": {"distance": 10},
        "2024-10-23": {"distance": 10},
        "2024-10-24": {"distance": 11},
        "2024-10-25": {"skipped": "Hang w/ G"},
        "2024-10-26": {"distance": 14},
        "2024-10-27": {"distance": 9},
        "2024-10-28": {"distance": 7},
        "2024-10-29": {"distance": 16},
        "2024-10-30": {"distance": 10},
        "2024-10-31": {"distance": 13},
        "2024-11-01": {"distance": 15},
        "2024-11-02": {"distance": 10},
        "2024-11-03": {"skipped": "Hang w/ G"},
        "2024-11-04": {"distance": 16},
        "2024-11-05": {"distance": 11},
        "2024-11-06": {"distance": 13},
        "2024-11-07": {"distance": 17},
        "2024-11-08": {"distance": 12},
        # 2024-11-09 is first use of Strava
        "2024-11-11": {"skipped": "Lazy?"},
        "2024-11-13": {"distance": 10},
        "2024-11-14": {"skipped": "Weather"},
        "2024-11-17": {"distance": 1.3, "op": "add"},  # Hercules
        "2024-11-21": {"skipped": "Lazy?"},
        "2024-11-24": {"distance": 11},  # Hercules/Pinole, w G
        "2024-11-25": {"skipped": "Weather"},
        "2024-11-27": {"distance": 16.3, "total_elevation_gain": 300, "op": "add"},  # return half of route not recorded by Strava
        "2024-12-16": {"skipped": "Weather"},
        "2024-12-18": {"distance": 12, "op": "add"},
        "2024-12-20": {"skipped": "Sick"},
        "2024-12-22": {"distance": 2.6, "total_elevation_gain": 566, "start_latlng": [37.990, -121.855], "op": "add"},  # initial, uphill part of route not recorded by Strava
        "2025-01-02": {"distance": 11.83},  # w G
    }

    def __init__(self, params):
        self.date_range = self.manual_data_date_range()
        self.params = params

    def manual_data_date_range(self):
        manual_dates = sorted(self.manual_data.keys())
        date_range = [
            ymd2date(manual_dates[0]),
            ymd2date(manual_dates[-1]),
        ]

        return date_range

    def get_strava_data(self):
        data = {}
        cache_name = self.params.cache_name

        activities = get_activities()
        for activity in activities:
            ymd = activity["start_date_local"][:10]

            # hack to convert starting location
            lat, lng = activity["start_latlng"]
            if approx_equal(lat, 37.96) and approx_equal(lng, -121.94):
                lat, lng = 37.96039, -121.94409  # nonsense location, but it has the right elevation

            elevation = get_elevation(cache_name, lat, lng)

            record = dict(
                ymd=ymd,
                distance=meters2miles(activity["distance"]),
                total_elevation_gain=meters2feet(activity["total_elevation_gain"]),
                average_speed=mps2mph(activity["average_speed"]),
                max_speed=mps2mph(activity["max_speed"]),
                elev_high=meters2feet(activity["elev_high"]),
                elev_low=meters2feet(activity["elev_low"]),
                elev_start=meters2feet(elevation),
            )
            data[ymd] = record

            dt = ymd2date(ymd)
            if dt < self.date_range[0]:
                self.date_range[0] = dt
            elif dt > self.date_range[1]:
                self.date_range[1] = dt

        return data

    def get_normalized_strava_data(self):
        strava_data = self.get_strava_data()

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
        if "skipped" in manual_record:
            return

        if "op" in manual_record and manual_record["op"] == "add":
            record["distance"] += manual_record.get("distance", 0)
            record["total_elevation_gain"] += manual_record.get("total_elevation_gain", 0)
        else:
            if "distance" in manual_record:
                record["distance"] = manual_record["distance"]
            if "total_elevation_gain" in manual_record:
                record["total_elevation_gain"] = manual_record["total_elevation_gain"]

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
