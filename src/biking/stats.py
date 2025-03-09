import calendar
import numpy as np

from .conversions import feet2miles, minutes2days, minutes2hours, period2days, ymd2date
from .format import format_numeric, format_metrics_record
from biking.power import output_power


def safe_div(a, b):
    return a / b if b else 0


class Statistics:
    def __init__(self, params, period, input_data, summary_info):
        self.params = params
        self.period = period
        self.input_data = input_data
        self.summary_info = summary_info
        self.text = []

        self.num_data_tracked_days = 0  # based on availability of speed and elevation data from Strava

        self.total_power = 0  # watts
        self.total_work = 0  # kJ
        self.total_calories = 0  # kCal

        self.stats = self.calculate()
        self.capture_summary_info()

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

    def energy_efficiency_adjustment(self, calories_per_day):
        min_e = self.params.calories.min_work_efficiency
        max_e = self.params.calories.max_work_efficiency
        divisor = (min_e + max_e) / 2

        return [n / divisor for n in calories_per_day]

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
            self.energy_efficiency_adjustment(data["calories_per_day"][-num:]),
            self.energy_efficiency_adjustment(data["avg_calories_per_day"][-num:]),
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

    def format_numeric(self, number, decimals=0):
        return format_numeric(number, "", True, decimals)

    def summarize_basic_data(self):
        stats = self.stats
        days = self.summary_info["days"]

        num_days = stats["num_days"]
        num_biked_days = stats["num_biked_days"]

        days["total"] += [num_days]
        days["biked"] += [num_biked_days]
        days["tracked"] += [stats["num_data_tracked_days"]]
        days["skipped"] += [num_days - num_biked_days]
        days["ride_rate"] += [self.format_numeric(num_biked_days / num_days * 100, 1)]

    def summarize_distance_data(self):
        stats = self.stats
        data = stats["data"]

        def min_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmin(x)

        def max_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmax(x)

        measure = self.summary_info["distance"]

        measure["min"] += [self.format_numeric(min_val("distance_per_day"), 1)]
        measure["max"] += [self.format_numeric(max_val("distance_per_day"), 1)]
        measure["avg"] += [self.format_numeric(safe_div(stats["total_distance"], stats["num_biked_days"]), 1)]
        measure["total"] += [self.format_numeric(stats["total_distance"], 0)]

    def summarize_time_data(self):
        stats = self.stats
        data = stats["data"]

        def min_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmin(x)

        def max_val(field):
            x = np.array([a if a else np.nan for a in data[field]])
            return 0 if np.all(np.isnan(x)) else np.nanmax(x)

        measure = self.summary_info["time"]

        measure["min"] += [self.format_numeric(min_val("time_per_day"), 0)]
        measure["max"] += [self.format_numeric(max_val("time_per_day"), 0)]
        measure["avg"] += [self.format_numeric(safe_div(stats["total_time"], stats["num_biked_days"]), 0)]
        measure["total"] += [self.format_numeric(stats["total_time"], 0)]
        measure["total_hours"] += [self.format_numeric(minutes2hours(stats["total_time"]), 1)]
        measure["total_days"] += [self.format_numeric(minutes2days(stats["total_time"]), 2)]

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
        avg_speed = safe_div(sum_vals("speed_per_day"), num_data_tracked_days)

        measure = self.summary_info["speed"]
        measure["min"] += [self.format_numeric(min_speed, 1)]
        measure["max"] += [self.format_numeric(max_speed, 1)]
        measure["avg"] += [self.format_numeric(avg_speed, 1)]

        # top speed
        min_top_speed = min_val("top_speed_per_day")
        max_top_speed = max_val("top_speed_per_day")
        avg_top_speed = safe_div(sum_vals("top_speed_per_day"), num_data_tracked_days)

        measure = self.summary_info["top_speed"]
        measure["min"] += [self.format_numeric(min_top_speed, 1)]
        measure["max"] += [self.format_numeric(max_top_speed, 1)]
        measure["avg"] += [self.format_numeric(avg_top_speed, 1)]

        # elevation gain
        total_elev_gain = int(sum_vals("elevation_gain_per_day"))
        total_elev_gain_miles = feet2miles(total_elev_gain)
        min_elev_gain = int(min_val("elevation_gain_per_day"))
        max_elev_gain = int(max_val("elevation_gain_per_day"))
        avg_elev_gain = int(safe_div(total_elev_gain, num_data_tracked_days))

        measure = self.summary_info["elevation_gain"]
        measure["min"] += [self.format_numeric(min_elev_gain, 0)]
        measure["max"] += [self.format_numeric(max_elev_gain, 0)]
        measure["avg"] += [self.format_numeric(avg_elev_gain, 0)]
        measure["total"] += [self.format_numeric(total_elev_gain, 0)]
        measure["total_miles"] += [self.format_numeric(total_elev_gain_miles, 1)]

        # elevation high
        min_elev_high = int(min_val("elevation_high_per_day"))
        max_elev_high = int(max_val("elevation_high_per_day"))
        avg_elev_high = int(sum_vals("elevation_high_per_day") / num_data_tracked_days)

        measure = self.summary_info["elevation_high"]
        measure["min"] += [self.format_numeric(min_elev_high, 0)]
        measure["max"] += [self.format_numeric(max_elev_high, 0)]
        measure["avg"] += [self.format_numeric(avg_elev_high, 0)]

        # elevation low
        min_elev_low = int(min_val("elevation_low_per_day"))
        max_elev_low = int(max_val("elevation_low_per_day"))
        avg_elev_low = int(sum_vals("elevation_low_per_day") / num_data_tracked_days)

        measure = self.summary_info["elevation_low"]
        measure["min"] += [self.format_numeric(min_elev_low, 0)]
        measure["max"] += [self.format_numeric(max_elev_low, 0)]
        measure["avg"] += [self.format_numeric(avg_elev_low, 0)]

        # power
        min_power = min_val("power_per_day")
        max_power = max_val("power_per_day")
        avg_power = safe_div(sum_vals("power_per_day"), num_data_tracked_days)

        measure = self.summary_info["power"]
        measure["min"] += [self.format_numeric(min_power, 0)]
        measure["max"] += [self.format_numeric(max_power, 0)]
        measure["avg"] += [self.format_numeric(avg_power, 0)]

        # work
        min_work = min_val("work_per_day")
        max_work = max_val("work_per_day")
        avg_work = safe_div(sum_vals("work_per_day"), num_data_tracked_days)

        measure = self.summary_info["work"]
        measure["min"] += [self.format_numeric(min_work, 0)]
        measure["max"] += [self.format_numeric(max_work, 0)]
        measure["avg"] += [self.format_numeric(avg_work, 0)]

        # energy
        data["adjusted_calories_per_day"] = self.energy_efficiency_adjustment(data["calories_per_day"])
        min_energy = min_val("adjusted_calories_per_day")
        max_energy = max_val("adjusted_calories_per_day")
        avg_energy = safe_div(sum_vals("adjusted_calories_per_day"), num_data_tracked_days)
        del data["adjusted_calories_per_day"]

        measure = self.summary_info["energy"]
        measure["min"] += [self.format_numeric(min_energy, 0)]
        measure["max"] += [self.format_numeric(max_energy, 0)]
        measure["avg"] += [self.format_numeric(avg_energy, 0)]

    @staticmethod
    def init_summary_info():
        return dict(
            days=dict(
                total=[],
                biked=[],
                tracked=[],
                skipped=[],
                ride_rate=[],
            ),
            distance=dict(
                min=[],
                max=[],
                avg=[],
                total=[],
            ),
            time=dict(
                min=[],
                max=[],
                avg=[],
                total=[],
                total_hours=[],
                total_days=[],
            ),
            speed=dict(
                min=[],
                max=[],
                avg=[],
            ),
            top_speed=dict(
                min=[],
                max=[],
                avg=[],
            ),
            elevation_gain=dict(
                min=[],
                max=[],
                avg=[],
                total=[],
                total_miles=[],
            ),
            elevation_high=dict(
                min=[],
                max=[],
                avg=[],
            ),
            elevation_low=dict(
                min=[],
                max=[],
                avg=[],
            ),
            power=dict(
                min=[],
                max=[],
                avg=[],
            ),
            work=dict(
                min=[],
                max=[],
                avg=[],
            ),
            energy=dict(
                min=[],
                max=[],
                avg=[],
            ),
        )

    def capture_summary_info(self):
        num_days = self.stats["num_days"]
        num_data_tracked_days = self.stats["num_data_tracked_days"]

        if num_days > 0:
            self.summarize_basic_data()
            self.summarize_distance_data()
            self.summarize_time_data()
            if num_data_tracked_days > 0:
                self.summarize_tracked_data()

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
                "{:7}  {:8}  {:8}  {:8}  "
                "{:9}"
            )
            row_format = (
                "{num:>4}  {ymd}  {distance:>8}  {avg_distance:>8}  "
                "{time:>8}  {avg_time:>8}  "
                "{speed:>7}  {avg_speed:>9}  {top_speed:>9}  {avg_top_speed:>13}  "
                "{elevation:>9}  {avg_elevation:>8}  {power:>5}  {avg_power:>9}  "
                "{work:>7}  {avg_work:>8}  {calories:>8}  {avg_calories:>8}  "
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
                    "-------  --------  --------  --------  "
                    "---------"
                )
            ymd = rec["date"].strftime("%Y-%m-%d")
            rec = format_metrics_record(rec, empty, limit_precision)
            msg = row_format.format(num=num, ymd=ymd, **rec)
            print(msg)
