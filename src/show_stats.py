#!/usr/bin/env python

import calendar
import matplotlib.pyplot as plt
import numpy as np
import os
import re

from datetime import date, timedelta
from typing import Union, List


config = dict(
    graph_file = "DailyMileage.jpg",
    input_path="images",
    output_path="output",
)


def parse_raw_data(path):
    daily_mileage = dict()  # "yyyymmdd" => num_miles
    date_range = None

    for file in os.listdir(path):
        # eg: bike-route-20241011-10mi.png
        m = re.match(r"bike-route-(\d\d\d\d)(\d\d)(\d\d)-(\d\d)mi.png", file)
        if m:
            yyyy = m.group(1)
            mm = m.group(2)
            dd = m.group(3)
            miles = int(m.group(4))

            ymd = f"{yyyy}-{mm}-{dd}"
            daily_mileage[ymd] = miles

            dt = date(int(yyyy), int(mm), int(dd))
            if date_range is None:
                date_range = [dt, dt]
            elif dt < date_range[0]:
                date_range[0] = dt
            elif dt > date_range[1]:
                date_range[1] = dt

    # simulate_add_extra_days(daily_mileage, date_range, 10, [10, 20])
    # simulate_add_extra_days_and_miles(daily_mileage, date_range, 63, 14)

    return daily_mileage, date_range


def simulate_add_extra_days_and_miles(daily_mileage, date_range, num_days, mileage):
    cur_date = date_range[1]

    for _ in range(num_days):
        cur_date += timedelta(days=1)
        ymd = cur_date.strftime("%Y-%m-%d")
        daily_mileage[ymd] = mileage
        mileage += 1

    date_range[1] = cur_date


def simulate_add_extra_days(daily_mileage, date_range, num_days, mileage: Union[int, List[int]]):
    cur_date = date_range[1]

    if isinstance(mileage, int):
        mileage = [mileage]

    mileage_offset = 0
    for _ in range(num_days):
        cur_date += timedelta(days=1)
        ymd = cur_date.strftime("%Y-%m-%d")
        daily_mileage[ymd] = mileage[mileage_offset]
        mileage_offset = (mileage_offset + 1) % len(mileage)

    date_range[1] = cur_date


def calculate_stats(path):
    daily_mileage, date_range = parse_raw_data(path)
    first_date, last_date = date_range
    first_day_of_week = calendar.weekday(first_date.year, first_date.month, first_date.day)

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
    )

    cur_date = first_date
    while cur_date <= last_date:
        ymd = cur_date.strftime("%Y-%m-%d")

        num_days += 1
        miles = 0
        if ymd in daily_mileage:
            miles = daily_mileage[ymd]
            num_biked_days += (1 if miles else 0)

        if 0 < miles < min_miles:
            min_miles = miles
        max_miles = max(miles, max_miles)
        total_miles += miles

        data["ride_rate_per_day"].append((num_biked_days * 100)/num_days)
        data["daily_mileage_per_day"].append(miles)
        data["avg_daily_mileage_per_day"].append(total_miles/num_days)
        data["avg_ride_day_mileage_per_day"].append(total_miles/num_biked_days)

        cur_date += timedelta(days=1)

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


def report_stats(stats):
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

    #ride_rate = stats["data"]["ride_rate"][-1]
    #avg_miles =  stats["data"]["avg_daily_mileage_per_day"][-1]
    #avg_ride_day_miles =  stats["data"]["avg_ride_day_mileage_per_day"][-1]
    ride_rate = round(num_biked_days / num_days * 100, 2)
    avg_miles = total_miles / num_days
    avg_ride_day_miles = total_miles / num_biked_days

    print(f"Date range: {first_day} to {last_day}")
    print()
    print("total days  biked  skipped  % biked")
    print("----------  -----  -------  -------")
    print(f"{num_days:10}  {num_biked_days:5}  {num_skipped_days:7}  {ride_rate:5.2f}%")
    print()
    print("biked miles  min  max   avg   avg-per-day-biked")
    print("-----------  ---  ---  -----  -----------------")
    print(f"{total_miles:11}  {min_miles:3}  {max_miles:3}  {avg_miles:5.1f}  {avg_ride_day_miles:17.1f}")
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
    plt.xticks(tick_offsets, tick_labels)


def y_axis_miles(stats, ax1):
    num_days = stats["num_days"]
    y = stats["data"]["daily_mileage_per_day"]
    avg_y = stats["data"]["avg_daily_mileage_per_day"]
    avg_ride_day_y = stats["data"]["avg_ride_day_mileage_per_day"]

    x = list(range(num_days))

    color = plt.cm.Greens(0.8)
    ax1.set_ylabel("Miles", color=color)
    plt.ylim(0, max(y))
    plt.yticks(range(0, int(max(y)) + 1, 1), color=color)

    plt.grid(axis="y", linestyle="-", alpha=0.15)

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
    plt.yticks(range(0, 101, 10), color=color)

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
    input_path = config["input_path"]
    stats = calculate_stats(input_path)
    report_stats(stats)

    output_path = config["output_path"]
    graph_file = config["graph_file"]
    plot_daily_miles(stats, f"{output_path}/{graph_file}")


main()
