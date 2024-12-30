#!/usr/bin/env python

import calendar
import matplotlib.pyplot as plt
import numpy as np
import os
import re

from datetime import date, timedelta
#from typing import Union, List

from strava import get_activities


def meters2feet(num):
    return float(num) * 3.28084


def meters2miles(num):
    return float(num) / 1609.34


def mps2mph(num):
    return float(num) * 2.23694


def ymd2date(ymd):
    dt = None

    m = re.match(r"(\d\d\d\d)-(\d\d)-(\d\d)", ymd)
    if m:
        yyyy = m.group(1)
        mm = m.group(2)
        dd = m.group(3)
        dt = date(int(yyyy), int(mm), int(dd))

    return dt


class Parameters:
    def __init__(self):
        self.output_path = "output"
        self.files = dict(
            mileage="DailyMileage.jpg",
            elevation_gain="DailyElevationGain.jpg",
            avg_speed="DailyAvgSpeed.jpg",
        )

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])


class InputData:
    # used to capture info on skipped days and rides prior to the use of Strava
    # ...or days when *someone* forgets to record a route using Strava
    manual_data = {
        "2024-10-11": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-12": {"distance": 6.9, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-13": {"distance": 9, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-14": {"distance": 11, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-15": {"distance": 11, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-16": {"distance": 11, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-17": {"distance": 13, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-18": {"distance": 14, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-19": {"distance": 23, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-20": {"distance": 8, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-21": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-22": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-23": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-24": {"distance": 11, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-25": {"skipped": "Hang w/ George"},
        "2024-10-26": {"distance": 14, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-27": {"distance": 9, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-28": {"distance": 7, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-29": {"distance": 16, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-30": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-10-31": {"distance": 13, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-01": {"distance": 15, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-02": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-03": {"skipped": "Hang w/ George"},
        "2024-11-04": {"distance": 16, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-05": {"distance": 11, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-06": {"distance": 13, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-07": {"distance": 17, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-08": {"distance": 12, "total_elevation_gain": 200, "average_speed": 8},
        # 2024-11-09 is first use of Strava
        "2024-11-11": {"skipped": "Lazy?"},
        "2024-11-13": {"distance": 10, "total_elevation_gain": 200, "average_speed": 8},
        "2024-11-14": {"skipped": "Weather"},
        "2024-11-17": {"op": "add", "distance": 1.3, "total_elevation_gain": 50, "average_speed": 9},  # Hercules
        "2024-11-21": {"skipped": "Lazy?"},
        "2024-11-24": {"distance": 11, "total_elevation_gain": 600, "average_speed": 9},  # Hercules/Pinole, w George
        "2024-11-25": {"skipped": "Weather"},
        "2024-11-27": {"op": "add", "distance": 16.3, "total_elevation_gain": 300, "average_speed": 9},  # Hercules
        "2024-12-16": {"skipped": "Weather"},
        "2024-12-18": {"op": "add", "distance": 12, "total_elevation_gain": 200, "average_speed": 8},
        "2024-12-20": {"skipped": "Sick"},
    }

    def __init__(self):
        self.date_range = self.manual_data_date_range()

    def manual_data_date_range(self):
        manual_dates = sorted(self.manual_data.keys())
        date_range = [
            ymd2date(manual_dates[0]),
            ymd2date(manual_dates[-1]),
        ]

        return date_range

    def get_strava_data(self):
        data = {}
        activities = get_activities()
        for activity in activities:
            ymd = activity["start_date_local"][:10]

            record = dict(
                ymd=ymd,
                distance=meters2miles(activity["distance"]),
                total_elevation_gain=meters2feet(activity["total_elevation_gain"]),
                average_speed=mps2mph(activity["average_speed"]),
                max_speed=mps2mph(activity["max_speed"]),
                elev_high=meters2feet(activity["elev_high"]),
                elev_low=meters2feet(activity["elev_low"]),
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
                )
            daily_data.append(record)

            cur_date += timedelta(days=1)

        return daily_data

    @staticmethod
    def apply_manual_record(record, manual_record):
        if "skipped" in manual_record:
            pass
        elif "op" in manual_record and manual_record["op"] == "add":
            record["distance"] += manual_record["distance"]
            record["total_elevation_gain"] += manual_record["total_elevation_gain"]
            ratio = record["distance"] / (record["distance"] + manual_record["distance"])
            record["average_speed"] = record["average_speed"] * ratio + manual_record["average_speed"] * (1 - ratio)
        else:
            record["distance"] = manual_record["distance"]
            record["total_elevation_gain"] = manual_record["total_elevation_gain"]
            record["average_speed"] = manual_record["average_speed"]

    def add_manual_data(self, daily_data):
        for record in daily_data:
            ymd = record["ymd"]
            if ymd in self.manual_data:
                manual_record = self.manual_data[ymd]
                self.apply_manual_record(record, manual_record)

    # def simulate_add_extra_days_and_miles(daily_mileage, date_range, num_days, mileage):
    #     cur_date = date_range[1]
    #
    #     for _ in range(num_days):
    #         cur_date += timedelta(days=1)
    #         ymd = cur_date.strftime("%Y-%m-%d")
    #         daily_mileage[ymd] = mileage
    #         mileage += 1
    #
    #     date_range[1] = cur_date
    #
    # def simulate_add_extra_days(daily_mileage, date_range, num_days, mileage: Union[int, List[int]]):
    #     cur_date = date_range[1]
    #
    #     if isinstance(mileage, int):
    #         mileage = [mileage]
    #
    #     mileage_offset = 0
    #     for _ in range(num_days):
    #         cur_date += timedelta(days=1)
    #         ymd = cur_date.strftime("%Y-%m-%d")
    #         daily_mileage[ymd] = mileage[mileage_offset]
    #         mileage_offset = (mileage_offset + 1) % len(mileage)
    #
    #     date_range[1] = cur_date

    def get_daily_data(self):
        daily_data = self.get_normalized_strava_data()
        self.add_manual_data(daily_data)

        # self.simulate_add_extra_days(daily_mileage, date_range, 10, [10, 20])
        # self.simulate_add_extra_days_and_miles(daily_mileage, date_range, 63, 14)

        return daily_data

    def summarize(self):
        print("date        miles  elevation  speed")
        print("----------  -----  ---------  -----")
        for rec in self.get_daily_data():
            if rec['distance']:
                print(f"{rec['ymd']}  {rec['distance']:5.1f}    {rec['total_elevation_gain']:5.0f}    {rec['average_speed']:5.1f}")
            else:
                print(rec['ymd'])


class Statistics:
    def __init__(self, input_data):
        self.input_data = input_data
        self.stats = self.calculate()

    def calculate(self):
        num_days = 0
        num_biked_days = 0

        max_miles = 0
        min_miles = 999
        total_miles = 0

        data = dict(
            ride_rate_per_day=[],
            daily_mileage_per_day=[],
            avg_daily_mileage_per_day=[],
            avg_ride_day_mileage_per_day=[],
            avg_speed_per_day=[],
            elevation_gain_per_day=[],
        )

        daily_data = self.input_data.get_daily_data()

        for record in daily_data:
            miles = record["distance"]
            num_days += 1
            num_biked_days += (1 if miles else 0)

            if 0 < miles < min_miles:
                min_miles = miles
            max_miles = max(miles, max_miles)
            total_miles += miles

            data["ride_rate_per_day"].append((num_biked_days * 100)/num_days)
            data["daily_mileage_per_day"].append(miles)
            data["avg_daily_mileage_per_day"].append(total_miles/num_days)
            data["avg_ride_day_mileage_per_day"].append(total_miles/num_biked_days)
            data["avg_speed_per_day"].append(record["average_speed"])
            data["elevation_gain_per_day"].append(record["total_elevation_gain"])

        first_date, last_date = self.input_data.date_range
        first_day_of_week = calendar.weekday(first_date.year, first_date.month, first_date.day)

        stats = dict(
            data=data,
            first_date=first_date,
            first_day_of_week=first_day_of_week,
            last_date=last_date,
            max_miles=max_miles,
            min_miles=min_miles,
            num_biked_days=num_biked_days,
            num_days=num_days,
            total_miles=total_miles,
        )

        return stats

    def report(self):
        stats = self.stats
        first_date = stats["first_date"]
        last_date = stats["last_date"]
        max_miles = stats["max_miles"]
        min_miles = stats["min_miles"]
        num_biked_days = stats["num_biked_days"]
        num_days = stats["num_days"]
        total_miles = stats["total_miles"]

        first_day = first_date.strftime("%Y-%m-%d")
        last_day = last_date.strftime("%Y-%m-%d")
        num_skipped_days = num_days - num_biked_days

        ride_rate = round(num_biked_days / num_days * 100, 2)
        avg_miles = total_miles / num_days
        avg_ride_day_miles = total_miles / num_biked_days

        print(f"Date range: {first_day} to {last_day}")
        print()
        print("total days  biked  skipped  ride rate")
        print("----------  -----  -------  ---------")
        print(f"{num_days:10}  {num_biked_days:5}  {num_skipped_days:7}  {ride_rate:8.2f}%")
        print()
        print("biked miles  min   max   avg   avg-per-day-biked")
        print("-----------  ----  ----  ----  -----------------")
        print(f"{total_miles:11.1f}  {min_miles:4.1f}  {max_miles:4.1f}  {avg_miles:4.1f}  {avg_ride_day_miles:17.1f}")
        print()


def get_ticks(num_days, period):
    offsets = [0] + [x - 1 for x in range(period, num_days, period)]
    if num_days % period != 1:
        offsets += [num_days - 1]
    labels = [str(x + 1) for x in offsets]

    return offsets, labels


def get_colors(stats):
    day_of_week = stats["first_day_of_week"]
    num_days = stats["num_days"]

    days_of_week = []

    for _ in range(num_days):
        days_of_week.append(day_of_week)
        day_of_week = (day_of_week + 1) % 7

    shades_of_green = plt.cm.Greens(np.linspace(0.3, 0.9, 7))
    colors = [shades_of_green[d] for d in days_of_week]

    return colors


def x_axis_days(stats, ax1):
    num_days = stats["num_days"]

    ax1.set_xlabel("Day (starting Oct 11, 2024)")
    tick_offsets, tick_labels = get_ticks(num_days, period=5)
    plt.xticks(tick_offsets, tick_labels, fontsize="x-small")


def y_axis_miles(stats, ax1):
    num_days = stats["num_days"]
    y = stats["data"]["daily_mileage_per_day"]
    avg_y = stats["data"]["avg_daily_mileage_per_day"]
    avg_ride_day_y = stats["data"]["avg_ride_day_mileage_per_day"]

    x = list(range(num_days))

    color = plt.cm.Greens(0.8)
    ax1.set_ylabel("Miles", color=color)
    plt.ylim(0, max(y))
    plt.yticks(range(0, int(max(y)) + 1, 1), color=color, fontsize="x-small")

    plt.grid(axis="y", linestyle="-", alpha=0.15, color=color)

    colors = get_colors(stats)

    ax1.bar(x, y, color=colors)
    line1, = ax1.plot(x, avg_y, color="lightblue", marker="o", markersize=5)
    line2, = ax1.plot(x, avg_ride_day_y, color="tab:blue", marker="o", markersize=3)

    return line1, line2


def y_axis_percentage(stats, ax1):
    num_days = stats["num_days"]
    ride_rate_y = stats["data"]["ride_rate_per_day"]

    x = list(range(num_days))

    color = "tab:red"
    ax2 = ax1.twinx()
    ax2.set_ylabel("Ride Rate", color=color)
    plt.ylim(0, max(ride_rate_y))
    plt.yticks(range(0, 101, 10), color=color, fontsize="x-small")

    for y in range(80, 100, 5):
        ax2.axhline(y, color=color, linestyle=":", alpha=0.25)

    line3, = plt.plot(x, ride_rate_y, color=color, marker="o", markersize=3)

    return line3


def legend(stats, line1, line2, line3):
    num_days = stats["num_days"]
    num_biked_days = stats["num_biked_days"]
    total_miles = stats["total_miles"]

    avg_miles = total_miles / num_days
    avg_ride_day_miles = total_miles / num_biked_days
    ride_rate = round(num_biked_days / num_days * 100, 2)

    plt.legend(
        loc="lower center",
        title="Legend: (latest value in parentheses)",
        title_fontsize="x-small",
        handles=(line1, line2, line3),
        labels=(
            f"Average Daily Miles ({avg_miles:0.1f})",
            f"Average Ride Day Miles ({avg_ride_day_miles:0.1f})",
            f"Ride Rate ({ride_rate:5.2f}%)",
        ),
    )


def plot_daily_miles(stats, graph_file):
    fig, ax1 = plt.subplots()
    plt.title("Bike Ride - Daily Mileage", pad=30)

    x_axis_days(stats, ax1)
    line1, line2 = y_axis_miles(stats, ax1)
    line3 = y_axis_percentage(stats, ax1)
    legend(stats, line1, line2, line3)

    plt.tight_layout()

    plt.savefig(graph_file, dpi=300)
    print(f"Daily Mileage per Day saved to {graph_file}.")
    print()


def main():
    parameters = Parameters()
    input_data = InputData()

    statistics = Statistics(input_data)
    statistics.report()

    plot_daily_miles(statistics.stats, parameters.file("mileage"))


main()
