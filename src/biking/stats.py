import calendar
import os

from .conversions import feet2miles, ymd2date
from biking.power import output_power


def safe_div(a, b):
    return a / b if b else 0


class Statistics:
    def __init__(self, params, input_data, period):
        self.params = params
        self.input_data = input_data
        self.period = period
        self.text = []

        self.num_data_tracked_days = 0   # based on availability of speed and elevation data from Strava

        self.total_power = 0  # watts
        self.total_energy = 0  # kJ
        self.total_calories = 0  # kCal

        self.stats = self.calculate(period)

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

        power, energy_jk, energy_kcal = 0, 0, 0
        if speed:
            power, energy_jk, energy_kcal = output_power(g, C_r, C_d, A, weight, elevation, speed, distance)

        return power, energy_jk, energy_kcal

    def add_derived_metrics(self, data, elevation, speed, distance):
        power, energy_kj, energy_kcal = self.power_based_metrics(elevation, speed, distance)

        self.total_power += power
        data["power_per_day"].append(power)
        data["avg_power_per_day"].append(safe_div(self.total_power, self.num_data_tracked_days))

        self.total_energy += energy_kj
        data["energy_per_day"].append(energy_kj)
        data["avg_energy_per_day"].append(safe_div(self.total_energy, self.num_data_tracked_days))

        self.total_calories += energy_kcal
        data["calories_per_day"].append(energy_kcal)
        data["avg_calories_per_day"].append(safe_div(self.total_calories, self.num_data_tracked_days))

    def calculate(self, period):
        num_days = 0
        num_biked_days = 0  # based on availability of distance info

        total_distance = 0  # miles
        total_speed = 0  # mph
        total_top_speed = 0  # mph
        total_elevation_gain = 0  # feet

        elevation_gain_per_day = []
        speed_per_day = []
        distance_per_day = []

        data = dict(
            date=[],

            ride_rate_per_day=[],

            distance_per_day=distance_per_day,
            avg_distance_per_day=[],

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
            energy_per_day=[],
            avg_energy_per_day=[],
            calories_per_day=[],
            avg_calories_per_day=[],
            strava_estimated_power_per_day=[],
        )

        daily_data = self.input_data.get_daily_data()

        report_num_days = self.params.report.num_days[period]
        factor_all_days = self.params.report.factor_all_days[period]
        if not factor_all_days and report_num_days is not None:
            daily_data = daily_data[-report_num_days:]

        for record in daily_data:
            distance = record["distance"]
            total_distance += distance

            speed = record["average_speed"]
            total_speed += speed

            top_speed = record["max_speed"]
            total_top_speed += top_speed

            elevation = record["total_elevation_gain"]
            total_elevation_gain += elevation

            num_days += 1
            num_biked_days += (1 if distance else 0)
            self.num_data_tracked_days += (1 if speed and elevation else 0)

            data["date"].append(record["date"])

            ride_rate = num_biked_days * 100 / num_days
            data["ride_rate_per_day"].append(ride_rate)

            data["distance_per_day"].append(distance)
            data["avg_distance_per_day"].append(safe_div(total_distance, num_biked_days))

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
            total_elevation_gain=total_elevation_gain,
        )

        return stats

    def report_basic_data(self):
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
        self.print(f"{num_days:11}  {num_biked_days:5}  {num_data_tracked_days:5}  {num_skipped_days:7}  {ride_rate:8.2f}%")

    def report_distance_data(self):
        stats = self.stats
        data = stats["data"]

        min_val = lambda field: min(x for x in data[field] if x > 0)
        max_val = lambda field: max(data[field])

        min_distance = min_val("distance_per_day")
        max_distance = max_val("distance_per_day")

        total_distance = stats["total_distance"]
        num_biked_days = stats["num_biked_days"]
        avg_distance = total_distance / num_biked_days

        self.print()
        self.print()
        self.print("distance (miles)  min   max   avg   total")
        self.print("                  ----  ----  ----  -------")
        self.print(f"{min_distance:22.1f}  {max_distance:4.1f}  {avg_distance:4.1f}  {total_distance:7.1f}")

    def report_tracked_data(self):
        stats = self.stats
        data = stats["data"]
        num_data_tracked_days = stats["num_data_tracked_days"]

        min_val = lambda field: min(x for x in data[field] if x > 0)
        max_val = lambda field: max(data[field])
        sum_vals = lambda field: sum(data[field])

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
        self.print(f"{min_elev_gain:25}  {max_elev_gain:4}  {avg_elev_gain:4}  {total_elev_gain:7}  {total_elev_gain_miles:11.1f}")
        self.print()
        self.print("elevation range (ft)  low:  min   max   avg   high:  min   max   avg")
        self.print("                            ----  ----  ----         ----  ----  ----")
        self.print(f"{min_elev_low:31}  {max_elev_low:4}  {avg_elev_low:4}  {min_elev_high:12}  {max_elev_high:4}  {avg_elev_high:4}")

    def report(self):
        num_days = self.stats["num_days"]
        num_data_tracked_days = self.stats["num_data_tracked_days"]

        self.print("<pre>")

        if num_days > 0:
            self.report_basic_data()
            self.report_distance_data()
            if num_data_tracked_days > 0:
                self.report_tracked_data()
        else:
            self.print("No activity found to report on.")

        self.print("</pre>")
        self.save_results()

    def show(self):
        data = self.stats["data"]

        date_y = data["date"]
        dist_y = data["distance_per_day"]
        avg_dist_y = data["avg_distance_per_day"]
        speed_y = data["speed_per_day"]
        avg_speed_y = data["avg_speed_per_day"]
        elev_y = data["elevation_gain_per_day"]
        avg_elev_y = data["avg_elevation_gain_per_day"]

        zipped = zip(date_y, dist_y, avg_dist_y, speed_y, avg_speed_y, elev_y, avg_elev_y)
        print("date          distance  avg distance    speed  avg speed    elev  avg elev")
        print("----------    --------  ------------    -----  ---------    ----  --------")
        for date, dist, dist_a, speed, speed_a, elev, elev_a in zipped:
            ymd = date.strftime("%Y-%m-%d")
            print(f"{ymd}    {dist:8.1f}  {dist_a:12.1f}    {speed:5.1f}  {speed_a:5.1f}    {elev:4.0f}  {elev_a:8.0f}")
