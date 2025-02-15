from datetime import timedelta

import json

from .db import Db
from .conversions import ymd2date
from .elevation import Elevation
from .journal import Journal
from .rollup.daily import DailyRollup
from .strava import Strava


class InputData:
    def __init__(self, params):
        self.params = params
        self.journal = Journal(params)
        self.elevation = Elevation(params)
        self.db = Db(params)

    def get_cached_activities(self):
        rows = self.db.select_activities()
        data = {}

        for date, activities in rows:
            data[date] = activities

        return data

    def cache_activities(self, new_activities, activities_map):
        for activity in new_activities:
            date = activity["start_date_local"]
            if date in activities_map:
                self.db.update_activity(date, activity)
            else:
                self.db.insert_activity(date, activity)

    def load_activities(self):
        activities_map = self.get_cached_activities()

        strava = Strava(self.params.strava)
        new_activities = strava.get_new_activities(activities_map)
        self.cache_activities(new_activities, activities_map)

        # combine new activities with cached ones
        for activity in new_activities:
            date = activity["start_date_local"]
            activities_map[date] = activity

        activities = [activities_map[date] for date in sorted(activities_map.keys())]

        return activities

    def calculate_date_range(self, activities, journal):
        t0 = None
        t1 = None

        for activity in activities:
            ymd = activity["start_date_local"][:10]
            if t0 is None or ymd < t0:
                t0 = ymd
            if t1 is None or ymd > t1:
                t1 = ymd

        if journal:
            journal_dates = sorted(journal.keys())
            if journal_dates[0] < t0:
                t0 = journal_dates[0]
            if journal_dates[-1] > t1:
                t1 = journal_dates[-1]

        return ymd2date(t0), ymd2date(t1)

    def init_daily_data(self, from_date, to_date):
        daily_data = {}

        cur_date = from_date
        while cur_date <= to_date:
            ymd = cur_date.strftime("%Y-%m-%d")
            daily_data[ymd] = DailyRollup(self.params, ymd)
            cur_date += timedelta(days=1)

        return daily_data

    def consolidate_data_sources(self, activities, journal):
        from_date, to_date = self.calculate_date_range(activities, journal)
        daily_data = self.init_daily_data(from_date, to_date)

        for activity in activities:
            ymd = activity["start_date_local"][:10]
            elev_start_ft = self.elevation.calculate_activity_start(activity)
            daily_data[ymd].add_activity(activity, elev_start_ft)

        for ymd, record in journal.items():
            daily_data[ymd].add_manual_activity(record)

        rollups = sorted(daily_data.values(), key=lambda a: a.ymd)
        daily_data = [rollup.aggregate_values() for rollup in rollups]

        return daily_data

    def get_daily_data(self):
        activities = self.load_activities()
        journal = self.journal.load()
        daily_data = self.consolidate_data_sources(activities, journal)
        # self.debug(daily_data)

        return daily_data

    def debug(self, daily_data, day_numbers=None):
        for num, record in enumerate(daily_data, 1):
            print("@@@", num, record["ymd"])
            if day_numbers is None or num in day_numbers:
                print(json.dumps(record, indent=4))

    def show(self, csv=False):
        headings = ("day#", "date", "distance", "elevation gain", "speed")
        if csv:
            head_format = "{},{},{},{},{}"
            row_format = "{num},{ymd},{distance},{total_elevation_gain},{average_speed}"
        else:
            head_format = "{:4}  {:10}  {:8}  {:14}  {:5}"
            row_format = "{num:4}  {ymd}  {distance:8.1f}  {total_elevation_gain:14.0f}  {average_speed:5.1f}"

        print(head_format.format(*headings))
        if not csv:
            print("----  ----------  --------  --------------  -----")

        for num, rec in enumerate(self.get_daily_data(), 1):
            distance = round(rec.get("distance"), 1)
            total_elevation_gain = round(rec.get("total_elevation_gain"), 1)
            average_speed = round(rec.get("average_speed"), 1)
            msg = row_format.format(
                num=num,
                ymd=rec["ymd"],
                distance=distance,
                total_elevation_gain=total_elevation_gain,
                average_speed=average_speed,
            )
            print(msg)
