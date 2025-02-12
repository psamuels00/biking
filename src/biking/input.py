from datetime import timedelta

import json
import sqlite3

from biking.params import Parameters
from .conversions import ymd2date
from .elevation import Elevation
from .journal import Journal
from .rollup.daily import DailyRollup
from .strava import Strava


class InputData:
    def __init__(self, params):
        self.params = params
        self.date_range = None
        self.journal = Journal(params)
        self.elevation = Elevation(params)

    def set_date_range(self, activities, journal):
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

        self.date_range = (ymd2date(t0), ymd2date(t1))

    def init_daily_data(self):
        daily_data = {}

        cur_date = self.date_range[0]
        while cur_date <= self.date_range[1]:
            ymd = cur_date.strftime("%Y-%m-%d")
            daily_data[ymd] = DailyRollup(self.params, ymd)
            cur_date += timedelta(days=1)

        return daily_data

    def consolidate_data_sources(self, activities, journal):
        daily_data = self.init_daily_data()

        for activity in activities:
            ymd = activity["start_date_local"][:10]
            elev_start_ft = self.elevation.calculate_activity_start(activity)
            daily_data[ymd].add_activity(activity, elev_start_ft)

        for ymd, record in journal.items():
            daily_data[ymd].add_manual_activity(record)

        daily_data = [
            rollup.aggregate_values()
            for rollup in sorted(daily_data.values(), key=lambda a: a.ymd)
        ]

        return daily_data

    def get_cached_activities(self, conn):
        cursor = conn.cursor()

        cursor.execute("SELECT date, activities FROM activities")
        rows = cursor.fetchall()

        data = {}

        for date, activities_json in rows:
            data[date] = activities_json

        cursor.close()

        return data

    def cache_activities(self, activities):
        file = self.params.strava.db_cache.file
        conn = sqlite3.connect(file)
        cursor = conn.cursor()

        cached_activities = self.get_cached_activities(conn)

        for activity in activities:
            date = activity["start_date_local"]
            activity_str = json.dumps(activity)
            if date not in cached_activities:
                print(f"DB cache: add activity for {date}")
                cursor.execute("INSERT INTO activities (date, activities) VALUES (?, ?)", (date, activity_str))
            elif activity_str != cached_activities[date]:
                print(f"DB cache: update activity for {date}")
                cursor.execute("UPDATE activities set activities = ? WHERE date = ?", (activity_str, date))

        conn.commit()

    def get_daily_data(self):
        strava = Strava(self.params.strava)
        activities = strava.get_activities()
        self.cache_activities(activities)
        journal = self.journal.load()
        self.set_date_range(activities, journal)
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
            print(row_format.format(
                num=num,
                ymd=rec["ymd"],
                distance=distance,
                total_elevation_gain=total_elevation_gain,
                average_speed=average_speed,
            ))
