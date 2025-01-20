from datetime import timedelta

from .conversions import ymd2date
from .elevation import Elevation
from .journal import Journal
from .rollup.daily import DailyRollup
from .strava import get_activities


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

    def get_daily_data(self):
        activities = get_activities()
        journal = self.journal.load()
        self.set_date_range(activities, journal)
        daily_data = self.consolidate_data_sources(activities, journal)

        return daily_data

    def summarize(self):
        print("date        distance  elevation gain  speed")
        print("----------  --------  --------------  -----")
        for rec in self.get_daily_data():
            if rec["distance"]:
                print(f"{rec["ymd"]}  {rec["distance"]:8.1f}    {rec["total_elevation_gain"]:10.0f}    {rec["average_speed"]:5.1f}")
            else:
                print(rec["ymd"])