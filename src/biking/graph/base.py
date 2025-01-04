import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, stats, output_file):
        self.stats = stats
        self.num_days = stats["num_days"]
        self.output_file = output_file
        self.handles = None
        self.labels = None

    def get_ticks(self, period):
        offsets = [0] + [x - 1 for x in range(period, self.num_days, period)]
        if self.num_days % period != 1:
            offsets += [self.num_days - 1]
        labels = [str(x + 1) for x in offsets]

        return offsets, labels

    def get_colors(self, light=False):
        day_of_week = self.stats["first_day_of_week"]
        num_days = self.stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        linspace_params = (0.2, 0.5) if light else (0.3, 0.9)
        shades_of_green = plt.cm.Greens(np.linspace(*linspace_params, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def set_legend(self, handles, labels):
        plt.legend(
            loc="lower center",
            fontsize="small",
            title="Legend: (latest value in parentheses)",
            title_fontsize="small",
            handles=handles,
            labels=labels,
        )

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day (starting Oct 11, 2024)")
        tick_offsets, tick_labels = self.get_ticks(period=5)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small")

    def y_axis_ride_rate(self, ax1):
        ride_rate_y = self.stats["data"]["ride_rate_per_day"]

        x = list(range(self.num_days))

        color = "tab:red"
        ax2 = ax1.twinx()
        ax2.set_ylabel("Ride Rate", color=color)
        plt.ylim(0, max(ride_rate_y))
        plt.yticks(range(0, 101, 10), color=color, fontsize="x-small")

        for y in range(80, 100, 5):
            ax2.axhline(y, color=color, linestyle=":", alpha=0.25)

        line3, = plt.plot(x, ride_rate_y, color=color, marker="o", markersize=3)

        return line3

    def y_axis_distance(self, ax1):
        y = self.stats["data"]["distance_per_day"]
        avg_y = self.stats["data"]["avg_distance_per_day"]
        avg_ride_day_y = self.stats["data"]["avg_distance_per_ride_day"]

        x = list(range(self.num_days))

        color = plt.cm.Greens(0.8)
        ax1.set_ylabel("Miles", color=color)
        plt.ylim(0, max(y))
        plt.yticks(range(0, int(max(y)) + 1, 1), color=color, fontsize="x-small")

        plt.grid(axis="y", linestyle="-", alpha=0.15, color=color)

        colors = self.get_colors()

        ax1.bar(x, y, color=colors)
        line1, = ax1.plot(x, avg_y, color="lightblue", marker="o", markersize=5)
        line2, = ax1.plot(x, avg_ride_day_y, color="tab:blue", marker="o", markersize=3)

        return line1, line2

    def y_axis_elevation(self, ax1):
        y = self.stats["data"]["elevation_gain_per_day"]
        x = list(range(self.num_days))

        y = [round(n) for n in y]

        ax1.set_ylabel("Feet")
        plt.ylim(0, max(y))
        plt.yticks(range(0, int(max(y)) + 1, 100), fontsize="x-small")

        plt.grid(axis="y", linestyle="-", alpha=0.15)

        colors = self.get_colors()
        ax1.bar(x, y, color=colors)
        dots1, = ax1.plot(x, y, color="blue", linestyle="None", marker="o", markersize=3)

        return dots1

    def y_axis_speed(self, ax1):
        y_avg = self.stats["data"]["avg_speed_per_day"]
        y_max = self.stats["data"]["max_speed_per_day"]
        x = list(range(self.num_days))

        # remove_zeroes = False
        # if remove_zeroes:
        #     x = []
        #     y_avg = []
        #     y_max = []
        #     y = zip(
        #         self.stats["data"]["avg_speed_per_day"],
        #         self.stats["data"]["max_speed_per_day"],
        #     )
        #     for n, (avg_value, max_value) in enumerate(y):
        #         if avg_value and max_value:
        #             x.append(n)
        #             y_avg.append(avg_value)
        #             y_max.append(max_value)

        ax1.set_ylabel("Miles/Hour")
        plt.ylim(0, max(y_max))
        plt.yticks(range(0, int(max(y_max)) + 1, 1), fontsize="x-small")

        plt.grid(axis="y", linestyle="-", alpha=0.15)

        colors = self.get_colors(True)
        ax1.vlines(x, ymin=y_avg, ymax=y_max, color=colors, linewidth=3)#, alpha=0.25)
        dots1, = ax1.plot(x, y_max, color="red", linestyle="None", marker="o", markersize=2)
        dots2, = ax1.plot(x, y_avg, color="blue", linestyle="None", marker="o", markersize=2)

        return dots1, dots2