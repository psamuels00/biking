import calendar
import os

from sympy.physics.units import frequency

from .conversions import feet2miles, ymd2date


def safe_div(a, b):
    return a / b if b else 0


class Statistics:
    def __init__(self, params, input_data, frequency, period):
        self.params = params
        self.input_data = input_data
        self.frequency = frequency
        self.period = period
        self.stats = self.calculate(period)
        self.text = []

    def print(self, line="<br>"):
        self.text.append(line)

    def save_results(self):
        path = os.path.join(self.params.summary.output_path, self.frequency)
        os.makedirs(path, exist_ok=True)
        file = os.path.join(str(path), f"{self.period}.html")
        content = "\n".join(self.text) + "\n"
        with open(file, "w") as fh:
            fh.write(content)

    def calculate(self, period):
        num_days = 0
        num_biked_days = 0  # based on availability of distance info
        num_data_tracked_days = 0  # ...plus speed and elevation data from Strava

        total_distance = 0  # miles
        total_speed = 0  # mph
        total_top_speed = 0  # mph
        total_elevation_gain = 0  # feet

        data = dict(
            ride_rate_per_day=[],

            distance_per_day=[],
            avg_distance_per_day=[],

            speed_per_day=[],  # ie, average speed
            avg_speed_per_day=[],  # ie, average of averages
            top_speed_per_day=[],
            avg_top_speed_per_day=[],

            elevation_gain_per_day=[],
            avg_elevation_gain_per_day=[],
            elevation_high_per_day=[],
            elevation_low_per_day=[],
            elevation_start_per_day=[],
        )

        daily_data = self.input_data.get_daily_data()

        total_num_days = len(daily_data)

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
            num_data_tracked_days += (1 if speed and elevation else 0)

            ride_rate = num_biked_days * 100 / num_days
            data["ride_rate_per_day"].append(ride_rate)
            data["distance_per_day"].append(distance)
            data["avg_distance_per_day"].append(total_distance/num_biked_days)
            data["speed_per_day"].append(speed)
            data["avg_speed_per_day"].append(safe_div(total_speed, num_data_tracked_days))
            data["top_speed_per_day"].append(top_speed)
            data["avg_top_speed_per_day"].append(safe_div(total_top_speed, num_data_tracked_days))
            data["elevation_gain_per_day"].append(elevation)
            data["avg_elevation_gain_per_day"].append(safe_div(total_elevation_gain, num_data_tracked_days))
            data["elevation_high_per_day"].append(record["elev_high"])
            data["elevation_low_per_day"].append(record["elev_low"])
            data["elevation_start_per_day"].append(record["elev_start"])

        if factor_all_days and report_num_days is not None:
            for key in data:
                print(f"    {key} len(data[{key}]) = {len(data[key])}")
                data[key] = data[key][-report_num_days:]
                print(f"    {key} len(data[{key}]) = {len(data[key])}")
                print()

        first_date, last_date = None, None
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
            num_data_tracked_days=num_data_tracked_days,
            num_days=num_days,
            total_distance=total_distance,
            total_elevation_gain=total_elevation_gain,
            total_num_days=total_num_days,
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
