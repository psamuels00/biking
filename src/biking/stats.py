import calendar
import numpy as np
import os

from .conversions import feet2miles, minutes2days, minutes2hours, period2days, ymd2date
from .format import format_metrics_record
from biking.power import output_power


def safe_div(a, b):
    return a / b if b else 0


class Statistics:
    def __init__(self, params, period, input_data):
        self.params = params
        self.period = period
        self.input_data = input_data
        self.text = []

        self.num_data_tracked_days = 0  # based on availability of speed and elevation data from Strava

        self.total_power = 0  # watts
        self.total_work = 0  # kJ
        self.total_calories = 0  # kCal

        self.stats = self.calculate()

    def print(self, line="<br>"):
        self.text.append(line)

    def save_results(self):
        path = self.params.summary.output_path
        os.makedirs(path, exist_ok=True)
        file = os.path.join(path, f"{self.period}.html")
        content = "\n".join(self.text) + "\n"
        with open(file, "w") as fh:
            fh.write(content)

    def get_weight_params(self):
        power = self.params.power

        cyclist_accessories_oz = 0
        for _, weight_oz in power.cyclist_accessories_oz.items():
            cyclist_accessories_oz += weight_oz
        cyclist_weight = power.cyclist_weight_lbs + cyclist_accessories_oz / 16

        bike_accessories_oz = 0
        for _, weight_oz in power.bike_accessories_oz.items():
            bike_accessories_oz += weight_oz
        bike_weight = power.bike_weight_lbs + bike_accessories_oz / 16

        return cyclist_weight + bike_weight

    def power_based_metrics(self, elevation, speed, distance):
        g = self.params.power.constants.g
        C_r = self.params.power.constants.C_r
        C_d = self.params.power.constants.C_d
        A = self.params.power.constants.A
        weight = self.get_weight_params()

        power_w, work_kj, energy_kcal = 0, 0, 0
        if speed:
            power_w, work_kj, energy_kcal = output_power(g, C_r, C_d, A, weight, elevation, speed, distance)

        return power_w, work_kj, energy_kcal

    def add_derived_metrics(self, data, elevation, speed, distance):
        power_w, work_kj, energy_kcal = self.power_based_metrics(elevation, speed, distance)

        self.total_power += power_w
        data["power_per_day"].append(power_w)
        data["avg_power_per_day"].append(safe_div(self.total_power, self.num_data_tracked_days))

        self.total_work += work_kj
        data["work_per_day"].append(work_kj)
        data["avg_work_per_day"].append(safe_div(self.total_work, self.num_data_tracked_days))

        self.total_calories += energy_kcal
        data["calories_per_day"].append(energy_kcal)
        data["avg_calories_per_day"].append(safe_div(self.total_calories, self.num_data_tracked_days))

    def calculate(self):
        num_days = 0
        num_biked_days = 0  # based on availability of distance info

        total_distance = 0  # miles
        total_time = 0  # seconds
        total_speed = 0  # mph
        total_top_speed = 0  # mph
        total_elevation_gain = 0  # feet

        elevation_gain_per_day = []
        speed_per_day = []
        distance_per_day = []
        time_per_day = []

        data = dict(
            date=[],
            ride_rate_per_day=[],
            distance_per_day=distance_per_day,
            avg_distance_per_day=[],
            time_per_day=time_per_day,
            avg_time_per_day=[],
            speed_per_day=speed_per_day,  # ie, average speed
            avg_speed_per_day=[],  # ie, average of averages
            top_speed_per_day=[],
            avg_top_speed_per_day=[],
            elevation_gain_per_day=elevation_gain_per_day,
            avg_elevation_gain_per_day=[],
            elevation_high_per_day=[],
            elevation_low_per_day=[],
            elevation_start_per_day=[],
            power_per_day=[],
            avg_power_per_day=[],
            work_per_day=[],
            avg_work_per_day=[],
            calories_per_day=[],
            avg_calories_per_day=[],
            strava_estimated_power_per_day=[],
        )

        num = period2days(self.period)
        daily_data = self.input_data.get_daily_data(num)

        report_num_days = self.params.report.num_days[self.period]
        factor_all_days = self.params.report.factor_all_days[self.period]
        if not factor_all_days and report_num_days is not None:
            daily_data = daily_data[-report_num_days:]

        for record in daily_data:
            distance = record["distance"]
            total_distance += distance

            time = record["moving_time"]
            total_time += time

            speed = record["average_speed"]
            total_speed += speed

            top_speed = record["top_speed"]
            total_top_speed += top_speed

            elevation = record["total_elevation_gain"]
            total_elevation_gain += elevation

            num_days += 1
            num_biked_days += 1 if distance else 0
            self.num_data_tracked_days += 1 if speed and elevation else 0

            data["date"].append(record["date"])

            ride_rate = num_biked_days * 100 / num_days
            data["ride_rate_per_day"].append(ride_rate)

            data["distance_per_day"].append(distance)
            data["avg_distance_per_day"].append(safe_div(total_distance, num_biked_days))

            data["time_per_day"].append(time)
            data["avg_time_per_day"].append(safe_div(total_time, self.num_data_tracked_days))

            data["speed_per_day"].append(speed)
            data["avg_speed_per_day"].append(safe_div(total_speed, self.num_data_tracked_days))
            data["top_speed_per_day"].append(top_speed)
            data["avg_top_speed_per_day"].append(safe_div(total_top_speed, self.num_data_tracked_days))

            data["elevation_gain_per_day"].append(elevation)
            data["avg_elevation_gain_per_day"].append(safe_div(total_elevation_gain, self.num_data_tracked_days))
            data["elevation_high_per_day"].append(record["elev_high"])
            data["elevation_low_per_day"].append(record["elev_low"])
            data["elevation_start_per_day"].append(record["elev_start"])

            self.add_derived_metrics(data, elevation, speed, distance)

            data["strava_estimated_power_per_day"].append(record["power"])

        if factor_all_days and report_num_days is not None:
            for key in data:
                data[key] = data[key][-report_num_days:]

        first_date, last_date = None, None
        first_day_of_week = None
        if daily_data:
            first_date = ymd2date(daily_data[0]["ymd"])
            last_date = ymd2date(daily_data[-1]["ymd"])
            first_day_of_week = calendar.weekday(first_date.year, first_date.month, first_date.day)

        stats = dict(
            data=data,
            first_date=first_date,
            first_day_of_week=first_day_of_week,
            last_date=last_date,
            num_biked_days=num_biked_days,
            num_data_tracked_days=self.num_data_tracked_days,
            num_days=num_days,
            total_distance=total_distance,
            total_time=total_time,
            total_elevation_gain=total_elevation_gain,
        )

        return stats

    def metrics_data(self, num):
        data = self.stats["data"]

        metrics = (
            data["date"][-num:],
            data["distance_per_day"][-num:],
            data["avg_distance_per_day"][-num:],
            data["time_per_day"][-num:],
            data["avg_time_per_day"][-num:],
            data["speed_per_day"][-num:],
            data["avg_speed_per_day"][-num:],
            data["top_speed_per_day"][-num:],
            data["avg_top_speed_per_day"][-num:],
            data["elevation_gain_per_day"][-num:],
            data["avg_elevation_gain_per_day"][-num:],
            data["power_per_day"][-num:],
            data["avg_power_per_day"][-num:],
            data["work_per_day"][-num:],
            data["avg_work_per_day"][-num:],
            data["calories_per_day"][-num:],
            data["avg_calories_per_day"][-num:],
            data["ride_rate_per_day"][-num:],
        )

        columns = (
            "date",
            "distance",
            "avg_distance",
            "time",
            "avg_time",
            "speed",
            "avg_speed",
            "top_speed",
            "avg_top_speed",
            "elevation",
            "avg_elevation",
            "power",
            "avg_power",
            "work",
            "avg_work",
            "calories",
            "avg_calories",
            "ride_rate",
        )

        rows = [
            dict(zip(columns, row))
            for row in np.array(metrics).T
        ]

        return rows

    def summarize_basic_data(self):
        stats = self.stats

        first_date = stats["first_date"]
        last_date = stats["last_date"]
        num_days = stats["num_days"]
        num_biked_days = stats["num_biked_days"]
        num_data_tracked_days = stats["num_data_tracked_days"]

        first_day = first_date.strftime("%Y-%m-%d")
        last_day = last_date.strftime("%Y-%m-%d")
        num_skipped_days = num_days - num_biked_days
        ride_rate = num_biked_days / num_days * 100

        title = self.params.report.title[self.period]

        self.print(f"Period: {title}")
        self.print()
        self.print(f"Date range: {first_day} to {last_day}")
        self.print()
        self.print()
        self.print("days  total  biked  tracked  skipped  ride rate")
        self.print("      -----  -----  -------  -------  ---------")
        self.print(
            f"{num_days:11}  {num_biked_days:5}  {num_data_tracked_days:5}  {num_skipped_days:7}  {ride_rate:8.2f}%"
        )

    def summarize_distance_data(self):
        stats = self.stats
        data = stats["data"]

        def min_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmin(x)

        def max_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmax(x)

        min_distance = min_val("distance_per_day")
        max_distance = max_val("distance_per_day")

        total_distance = stats["total_distance"]
        num_biked_days = stats["num_biked_days"]
        avg_distance = safe_div(total_distance, num_biked_days)

        self.print()
        self.print()
        self.print("distance (miles)  min   max   avg   total")
        self.print("                  ----  ----  ----  -------")
        self.print(f"{min_distance:22.1f}  {max_distance:4.1f}  {avg_distance:4.1f}  {total_distance:7.1f}")

    def summarize_time_data(self):
        stats = self.stats
        data = stats["data"]

        def min_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmin(x)

        def max_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmax(x)

        min_time = int(min_val("time_per_day"))
        max_time = int(max_val("time_per_day"))

        total_time = int(stats["total_time"])
        total_days = minutes2days(stats["total_time"])
        total_hours = minutes2hours(stats["total_time"])
        num_biked_days = stats["num_biked_days"]
        avg_time = int(safe_div(stats["total_time"], num_biked_days))

        self.print()
        self.print()
        self.print("time (minutes)  min   max   avg   total    total hours  total days")
        self.print("                ----  ----  ----  -------  -----------  ----------")
        self.print(
            f"{min_time:20}  {max_time:4}  {avg_time:4}  {total_time:7}  {total_hours:11.1f}  {total_days:10.1f}"
        )

    def summarize_tracked_data(self):
        stats = self.stats
        data = stats["data"]
        num_data_tracked_days = stats["num_data_tracked_days"]

        def min_val(field):
            return min(x for x in data[field] if x > 0)

        def max_val(field):
            return max(data[field])

        def sum_vals(field):
            return sum(data[field])

        # speed
        min_speed = min_val("speed_per_day")
        max_speed = max_val("speed_per_day")
        avg_speed = sum_vals("speed_per_day") / num_data_tracked_days

        # top speed
        min_top_speed = min_val("top_speed_per_day")
        max_top_speed = max_val("top_speed_per_day")
        avg_top_speed = sum_vals("top_speed_per_day") / num_data_tracked_days

        # elevation gain
        total_elev_gain = int(sum_vals("elevation_gain_per_day"))
        total_elev_gain_miles = feet2miles(total_elev_gain)
        min_elev_gain = int(min_val("elevation_gain_per_day"))
        max_elev_gain = int(max_val("elevation_gain_per_day"))
        avg_elev_gain = int(total_elev_gain / num_data_tracked_days)

        # elevation low
        min_elev_low = int(min_val("elevation_low_per_day"))
        max_elev_low = int(max_val("elevation_low_per_day"))
        avg_elev_low = int(sum_vals("elevation_low_per_day") / num_data_tracked_days)

        # elevation high
        min_elev_high = int(min_val("elevation_high_per_day"))
        max_elev_high = int(max_val("elevation_high_per_day"))
        avg_elev_high = int(sum_vals("elevation_high_per_day") / num_data_tracked_days)

        self.print()
        self.print()
        self.print("speed (mph)  min   max   avg")
        self.print("             ----  ----  ----")
        self.print(f"{min_speed:17.1f}  {max_speed:4.1f}  {avg_speed:4.1f}")
        self.print()
        self.print("top speed (mph)  min   max   avg")
        self.print("                 ----  ----  ----")
        self.print(f"{min_top_speed:21.1f}  {max_top_speed:4.1f}  {avg_top_speed:4.1f}")
        self.print()
        self.print()
        self.print("elevation gain (ft)  min   max   avg   total    total miles")
        self.print("                     ----  ----  ----  -------  -----------")
        self.print(
            f"{min_elev_gain:25}  {max_elev_gain:4}  {avg_elev_gain:4}  "
            f"{total_elev_gain:7}  {total_elev_gain_miles:11.1f}"
        )
        self.print()
        self.print("elevation range (ft)  low:  min   max   avg   high:  min   max   avg")
        self.print("                            ----  ----  ----         ----  ----  ----")
        self.print(
            f"{min_elev_low:31}  {max_elev_low:4}  {avg_elev_low:4}  "
            f"{min_elev_high:12}  {max_elev_high:4}  {avg_elev_high:4}"
        )

    def summary(self):
        num_days = self.stats["num_days"]
        num_data_tracked_days = self.stats["num_data_tracked_days"]

        self.print("<pre>")

        if num_days > 0:
            self.summarize_basic_data()
            self.summarize_distance_data()
            self.summarize_time_data()
            if num_data_tracked_days > 0:
                self.summarize_tracked_data()
        else:
            self.print("No activity found to report on.")

        self.print("</pre>")
        self.save_results()

    def details(self, csv=False):
        headings = (
            "day#",
            "date",
            "distance",
            "avg dist",
            "time",
            "avg time",
            "speed",
            "avg speed",
            "top speed",
            "avg top speed",
            "elev gain",
            "avg elev",
            "power",
            "avg power",
            "work kj",
            "avg work",
            "calories",
            "avg cals",
            "ride rate",
        )

        if csv:
            head_format = ",".join(["{}"] * len(headings))
            row_format = (
                "{num},{ymd},{distance},{avg_distance},"
                "{time},{avg_time},"
                "{speed},{avg_speed},{top_speed},{avg_top_speed},"
                "{elevation},{avg_elevation},{power},{avg_power},"
                "{work},{avg_work},{calories},{avg_calories},"
                "{ride_rate}"
            )
            empty = ""
            limit_precision = False
            print(head_format.format(*headings))
        else:
            head_format = (
                "{:4}  {:10}  {:8}  {:8}  "
                "{:8}  {:8}  "
                "{:7}  {:9}  {:9}  {:13}  "
                "{:9}  {:8}  {:5}  {:9}  "
                "{:9}  {:10}  {:8}  {:8}  "
                "{:9}"
            )
            row_format = (
                "{num:>4}  {ymd}  {distance:>8}  {avg_distance:>8}  "
                "{time:>8}  {avg_time:>8}  "
                "{speed:>7}  {avg_speed:>9}  {top_speed:>9}  {avg_top_speed:>13}  "
                "{elevation:>9}  {avg_elevation:>8}  {power:>5}  {avg_power:>9}  "
                "{work:>9}  {avg_work:>10}  {calories:>8}  {avg_calories:>8}  "
                "{ride_rate:>9}"
            )
            empty = "."
            limit_precision = True

        num = period2days(self.period)
        rows = self.metrics_data(num)

        for num, rec in enumerate(rows, 1):
            if not csv and (num - 1) % 10 == 0:
                if num > 1:
                    print()
                print(head_format.format(*headings))
                print(
                    "----  ----------  --------  --------  "
                    "--------  --------  "
                    "-------  ---------  ---------  -------------  "
                    "---------  --------  -----  ---------  "
                    "---------  ----------  --------  --------  "
                    "---------"
                )
            ymd = rec["date"].strftime("%Y-%m-%d")
            rec = format_metrics_record(rec, empty, limit_precision)
            msg = row_format.format(num=num, ymd=ymd, **rec)
            print(msg)
