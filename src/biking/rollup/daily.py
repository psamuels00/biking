import numpy as np

from datetime import datetime

from biking.conversions import meters2feet, meters2miles, mps2mph, seconds2minutes
from .metric import Metric


class DailyRollup:
    def __init__(self, params, ymd):
        self.params = params

        self.ymd = ymd
        self.date = datetime.strptime(ymd, "%Y-%m-%d").date()
        self.distance = Metric()
        self.moving_time = Metric()
        self.total_elevation_gain = Metric()
        self.average_speed = Metric()
        self.top_speed = Metric()
        self.elev_high = Metric()
        self.elev_low = Metric()
        self.elev_start = Metric()
        self.power = Metric()

    def add_activity(self, activity, elev_start_ft):
        self.distance.add_measure(meters2miles(activity.get("distance", np.nan)))
        self.moving_time.add_measure(seconds2minutes(activity.get("moving_time", np.nan)))
        self.total_elevation_gain.add_measure(meters2feet(activity.get("total_elevation_gain", np.nan)))
        self.average_speed.add_measure(mps2mph(activity.get("average_speed", np.nan)))
        self.top_speed.add_measure(mps2mph(activity.get("max_speed", np.nan)))
        self.elev_high.add_measure(meters2feet(activity.get("elev_high", np.nan)))
        self.elev_low.add_measure(meters2feet(activity.get("elev_low", np.nan)))
        self.elev_start.add_measure(elev_start_ft)
        self.power.add_measure(0)

    def add_manual_activity(self, record, elev_start_ft, replace=False):
        self.distance.add_measure(record.get("distance", np.nan), replace)  # assumed to be miles
        self.moving_time.add_measure(record.get("moving_time", np.nan), replace)  # assumed to be minutes
        self.total_elevation_gain.add_measure(record.get("total_elevation_gain", np.nan), replace)  # assumed to be feet
        self.average_speed.add_measure(record.get("average_speed", np.nan), replace)  # assumed to be mph
        self.top_speed.add_measure(record.get("top_speed", np.nan), replace)  # assumed to be mph
        self.elev_high.add_measure(record.get("elev_high", np.nan), replace)  # assumed to be feet
        self.elev_low.add_measure(record.get("elev_low", np.nan), replace)  # assumed to be feet
        self.power.add_measure(record.get("strava_power_estimate", np.nan), replace)  # assumed to be in watts
        self.elev_start.add_measure(elev_start_ft, replace)

        if "replace" in record:
            self.add_manual_activity(record["replace"], elev_start_ft, replace=True)

    def aggregate_values(self):
        return dict(
            ymd=self.ymd,
            date=self.date,
            distance=self.distance.sum(),
            moving_time=self.moving_time.sum(),
            total_elevation_gain=self.total_elevation_gain.sum(),
            average_speed=self.average_speed.avg(),
            top_speed=self.top_speed.max(),
            elev_high=self.elev_high.max(),
            elev_low=self.elev_low.min(),
            elev_start=self.elev_start.last(),
            power=self.power.max(),
        )
