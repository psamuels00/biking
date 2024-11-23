#!/usr/bin/env python

import matplotlib.pyplot as plt
import os
import re

from datetime import date


def calculate_stats(path):
    first_date = None
    last_date = None

    num_biked_days = 0
    num_biked_miles = 0
    miles_per_day = []

    min_miles = 999
    max_miles = 0

    prev_date = None

    for file in sorted(os.listdir(path)):
        # eg: bike-route-20241011-10mi.png
        m = re.match(r"bike-route-(\d\d\d\d)(\d\d)(\d\d)-(\d\d)mi.png", file)
        if m:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            miles = int(m.group(4))

            route_date = date(year, month, day)

            if not first_date:
                first_date = route_date
            last_date = route_date

            num_biked_days += 1
            num_biked_miles += miles

            min_miles = min(miles, min_miles)
            max_miles = max(miles, max_miles)

            if prev_date:
                num_skipped_days = (route_date - prev_date).days - 1
                miles_per_day += [0] * num_skipped_days
            miles_per_day.append(miles)

            prev_date = route_date

    stats = dict(
        first_date=first_date,
        last_date=last_date,
        max_miles=max_miles,
        miles_per_day=miles_per_day,
        min_miles=min_miles,
        num_biked_days=num_biked_days,
        num_biked_miles=num_biked_miles,
    )

    return stats


def report_stats(stats):
    first_date = stats["first_date"]
    last_date = stats["last_date"]
    max_miles = stats["max_miles"]
    min_miles = stats["min_miles"]
    num_biked_days = stats["num_biked_days"]
    num_biked_miles = stats["num_biked_miles"]

    first_day = first_date.strftime("%Y-%m-%d")
    last_day = last_date.strftime("%Y-%m-%d")
    num_total_days = (last_date - first_date).days + 1
    percent_biked_days = round(num_biked_days / num_total_days * 100)
    num_skipped_days = num_total_days - num_biked_days
    avg_miles = num_biked_miles / num_total_days
    avg_miles_per_day_biked = num_biked_miles / num_biked_days

    print(f"Date range: {first_day} to {last_day}")
    print()
    print("total days  biked  skipped  % biked")
    print("----------  -----  -------  -------")
    print(f"{num_total_days:10}  {num_biked_days:5}  {num_skipped_days:7}  {percent_biked_days:6}%")
    print()
    print("biked miles  min  max   avg   avg-per-day-biked")
    print("-----------  ---  ---  -----  -----------------")
    print(f"{num_biked_miles:11}  {min_miles:3}  {max_miles:3}  {avg_miles:5.1f}  {avg_miles_per_day_biked:17.1f}")
    print()


def plot_daily_miles(stats, graph_file):
    miles_per_day = stats["miles_per_day"]

    x = list(range(0, len(miles_per_day)))
    y = miles_per_day

    plt.bar(x, y, color="green")

    plt.xlabel("day")
    plt.ylabel("miles")
    plt.title("Daily Bike Ride")

    plt.savefig(graph_file)
    print(f"Daily Miles saved to {graph_file}.")
    print()


def main():
    path = "images"
    graph_file = "DailyBikeRide.jpg"

    stats = calculate_stats(path)
    report_stats(stats)
    plot_daily_miles(stats, graph_file)


main()
