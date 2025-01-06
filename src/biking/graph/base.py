import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime


class Graph:
    def __init__(self, stats, output_file):
        self.stats = stats
        self.num_days = stats["num_days"]
        self.output_file = output_file
        self.handles = []
        self.labels = []

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

    def title(self, metric):
        from_date = "Oct 11, 2024"
        to_date = datetime.now().strftime("%b %d, %Y")
        title = "\n".join([
            f"Daily Bike Ride - {metric}",
            f"{from_date} - {to_date}",
        ])

        plt.title(title, pad=30)

    def legend(self, loc="lower center"):
        plt.legend(
            loc=loc,
            fontsize="small",
            title="Legend: (latest value in parentheses)",
            title_fontsize="small",
            handles=self.handles,
            labels=self.labels,
        )

    def build(self, ax1):
        pass

    def generate(self):
        fig, ax1 = plt.subplots()
        self.build(ax1)
        plt.tight_layout()
        plt.savefig(self.output_file, dpi=300, bbox_inches="tight")

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day")
        tick_offsets, tick_labels = self.get_ticks(period=5)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small")

    def y_axis_ride_rate(self, ax1):
        x = list(range(self.num_days))
        ride_rate_y = self.stats["data"]["ride_rate_per_day"]

        min_ride_rate = int(max(0, min(ride_rate_y) // 5 * 5 - 5))
        bottom_limit = min_ride_rate
        scale = range(min_ride_rate, 101, 1)

        ax1.set_ylabel("Percentage")
        ax1.set_ylim(bottom_limit, max(ride_rate_y))
        ax1.set_yticks(scale, labels=scale, fontsize="x-small")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        ax2 = ax1.twinx()
        ax2.set_ylim(bottom_limit, max(ride_rate_y))
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.25)

        num_biked_days = self.stats["num_biked_days"]
        ride_rate = round(num_biked_days / self.num_days * 100, 2)
        line, = ax1.plot(x, ride_rate_y, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Ride Rate ({ride_rate:5.2f}%)")

    def y_axis_distance(self, ax1):
        x = list(range(self.num_days))
        y = self.stats["data"]["distance_per_day"]
        avg_y = self.stats["data"]["avg_distance_per_day"]
        avg_ride_day_y = self.stats["data"]["avg_distance_per_ride_day"]

        scale = range(0, int(max(y)) + 1, 1)

        ax1.set_ylabel("Miles")
        ax1.set_ylim(0, max(y))
        ax1.set_yticks(scale, labels=scale, fontsize="x-small")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        ax2 = ax1.twinx()
        ax2.set_ylim(0, max(y))
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.25)

        colors = self.get_colors()
        ax1.bar(x, y, color=colors)

        num_biked_days = self.stats["num_biked_days"]
        total_miles = self.stats["total_miles"]

        avg_miles = total_miles / self.num_days
        line, = ax1.plot(x, avg_y, color="lightblue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Distance per Day ({avg_miles:0.1f} mi)")

        avg_ride_day_miles = total_miles / num_biked_days
        line, = ax1.plot(x, avg_ride_day_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Distance per Ride Day ({avg_ride_day_miles:0.1f} mi)")

    def y_axis_elevation(self, ax1):
        x = list(range(self.num_days))
        y_gain = self.stats["data"]["elevation_gain_per_day"]
        y_high = self.stats["data"]["elevation_high_per_day"]
        y_low = self.stats["data"]["elevation_low_per_day"]

        y_gain = [round(n) for n in y_gain]
        y_high = [round(n) for n in y_high]
        y_low = [round(n) for n in y_low]

        max_y = int(max(*y_gain, *y_high))
        scale = range(0, max_y + 1, 100)

        ax1.set_ylabel("Feet")
        ax1.set_ylim(0, max_y)
        ax1.set_yticks(scale, labels=scale, fontsize="x-small")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        ax2 = ax1.twinx()
        ax2.set_ylim(0, max_y)
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.25)

        colors = self.get_colors()
        ax1.bar(x, y_gain, color=colors)

        elevation_gain = self.stats["data"]["elevation_gain_per_day"][-1]
        dots, = ax1.plot(x, y_gain, color="tab:blue", linestyle="None", marker="o", markersize=3)
        self.handles.append(dots)
        self.labels.append(f"Elevation Gain ({elevation_gain:0.1f} ft)")

        elevation_low = self.stats["data"]["elevation_low_per_day"][-1]
        line, = ax1.plot(x, y_low, color="yellow", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation Low ({elevation_low:0.1f} ft)")

        elevation_high = self.stats["data"]["elevation_high_per_day"][-1]
        line, = ax1.plot(x, y_high, color="orange", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation High ({elevation_high:0.1f} ft)")

    def y_axis_speed(self, ax1):
        x = list(range(self.num_days))
        y_avg = self.stats["data"]["avg_speed_per_day"]
        y_max = self.stats["data"]["max_speed_per_day"]

        scale = range(0, int(max(y_max)) + 1, 1)

        ax1.set_ylabel("Miles/Hour")
        ax1.set_ylim(0, max(y_max))
        ax1.set_yticks(scale, labels=scale, fontsize="x-small")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        ax2 = ax1.twinx()
        ax2.set_ylim(0, max(y_max))
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.25)

        colors = self.get_colors(True)
        ax1.vlines(x, ymin=y_avg, ymax=y_max, color=colors, linewidth=3)

        max_speed = self.stats["data"]["max_speed_per_day"][-1]
        dots, = ax1.plot(x, y_max, color="tab:red", linestyle="None", marker="o", markersize=2)
        self.handles.append(dots)
        self.labels.append(f"Max Speed ({max_speed:0.1f} mph)")

        avg_speed = self.stats["data"]["avg_speed_per_day"][-1]
        dots, = ax1.plot(x, y_avg, color="tab:blue", linestyle="None", marker="o", markersize=2)
        self.handles.append(dots)
        self.labels.append(f"Average Speed ({avg_speed:0.1f} mph)")
