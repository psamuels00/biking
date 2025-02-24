from datetime import date, timedelta

import json

from .db import Db
from .conversions import period2days, ymd2date
from .elevation import Elevation
from .format import format_input_record
from .journal import Journal
from .rollup.daily import DailyRollup
from .strava import Strava


class InputData:
    def __init__(self, params, period):
        self.params = params
        self.journal = Journal(params)
        self.elevation = Elevation(params)
        self.db = Db(params)
        self.daily_data = None
        self.period = period

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

        from_date = ymd2date(t0)
        to_date = date.today() if self.params.report.from_today else ymd2date(t1)

        return from_date, to_date

    def init_daily_data(self, from_date, to_date):
        daily_data = {}

        cur_date = from_date
        while cur_date <= to_date:
            ymd = cur_date.strftime("%Y-%m-%d")
            daily_data[ymd] = DailyRollup(self.params, ymd)
            cur_date += timedelta(days=1)

        return daily_data

    def include_activity(self, ymd):
        # return "2024-10-11" <= ymd <= "2025-01-24"  # for testing only
        return True

    def consolidate_data_sources(self, activities, journal):
        from_date, to_date = self.calculate_date_range(activities, journal)
        daily_data = self.init_daily_data(from_date, to_date)

        for activity in activities:
            ymd = activity["start_date_local"][:10]
            if self.include_activity(ymd):
                elev_start_ft = self.elevation.calculate_activity_start(activity)
                daily_data[ymd].add_activity(activity, elev_start_ft)

        for ymd, record in journal.items():
            if self.include_activity(ymd):
                daily_data[ymd].add_manual_activity(record)

        rollups = sorted(daily_data.values(), key=lambda a: a.ymd)
        daily_data = [rollup.aggregate_values() for rollup in rollups]

        return daily_data

    def get_daily_data(self, num):
        if not self.daily_data:
            activities = self.load_activities()
            journal = self.journal.load()
            self.daily_data = self.consolidate_data_sources(activities, journal)

        return self.daily_data[-num:]

    def debug(self, daily_data, day_numbers=None):
        for num, record in enumerate(daily_data, 1):
            print("@@@", num, record["ymd"])
            if day_numbers is None or num in day_numbers:
                print(json.dumps(record, indent=4))

    def details(self, csv=False):
        headings = (
            "day#",
            "date",
            "distance",
            "speed",
            "top speed",
            "elev gain",
            "elev high",
            "elev low",
            "elev start",
            "power",
        )

        if csv:
            head_format = ",".join(["{}"] * len(headings))
            row_format = (
                "{num},{ymd},{distance},{average_speed},{top_speed},"
                "{total_elevation_gain},{elev_high},{elev_low},{elev_start},{power}"
            )
            empty = ""
            limit_precision = False
            print(head_format.format(*headings))
        else:
            head_format = "{:4}  {:10}  {:8}  {:5}  {:9}  {:9}  {:9}  {:8}  {:10}  {:5}"
            row_format = (
                "{num:>4}  {ymd}  {distance:>8}  {average_speed:>5}  {top_speed:>9}  "
                "{total_elevation_gain:>9}  {elev_high:>9}  {elev_low:>8}  {elev_start:>10}  {power:>5}"
            )
            empty = "."
            limit_precision = True

        num = period2days(self.period)
        records = self.get_daily_data(num)

        for num, rec in enumerate(records, 1):
            if not csv and (num - 1) % 10 == 0:
                if num > 1:
                    print()
                print(head_format.format(*headings))
                print(
                    "----  ----------  --------  -----  ---------  ---------  ---------  --------  ----------  -----"
                )
            rec = format_input_record(rec, empty, limit_precision)
            msg = row_format.format(num=num, **rec)
            print(msg)
