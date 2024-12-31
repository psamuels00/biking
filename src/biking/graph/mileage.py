import matplotlib.pyplot as plt
import numpy as np


class MileageGraph:
    def __init__(self, stats, output_file):
        self.stats = stats
        self.output_file = output_file

    def get_ticks(self, num_days, period):
        offsets = [0] + [x - 1 for x in range(period, num_days, period)]
        if num_days % period != 1:
            offsets += [num_days - 1]
        labels = [str(x + 1) for x in offsets]

        return offsets, labels

    def get_colors(self, stats):
        day_of_week = stats["first_day_of_week"]
        num_days = stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        shades_of_green = plt.cm.Greens(np.linspace(0.3, 0.9, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def x_axis_days(self, stats, ax1):
        num_days = stats["num_days"]

        ax1.set_xlabel("Day (starting Oct 11, 2024)")
        tick_offsets, tick_labels = self.get_ticks(num_days, period=5)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small")

    def y_axis_miles(self, stats, ax1):
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

        colors = self.get_colors(stats)

        ax1.bar(x, y, color=colors)
        line1, = ax1.plot(x, avg_y, color="lightblue", marker="o", markersize=5)
        line2, = ax1.plot(x, avg_ride_day_y, color="tab:blue", marker="o", markersize=3)

        return line1, line2

    def y_axis_percentage(self, stats, ax1):
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

    def legend(self, stats, line1, line2, line3):
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

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Bike Ride - Daily Mileage", pad=30)

        self.x_axis_days(self.stats, ax1)
        line1, line2 = self.y_axis_miles(self.stats, ax1)
        line3 = self.y_axis_percentage(self.stats, ax1)
        self.legend(self.stats, line1, line2, line3)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Daily Mileage per Day saved to {self.output_file}.")
        print()
