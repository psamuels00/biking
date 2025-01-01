import matplotlib.pyplot as plt

from .base import Graph


class DistanceGraph(Graph):
    def y_axis_miles(self, ax1):
        y = self.stats["data"]["daily_mileage_per_day"]
        avg_y = self.stats["data"]["avg_daily_mileage_per_day"]
        avg_ride_day_y = self.stats["data"]["avg_ride_day_mileage_per_day"]

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

    def y_axis_percentage(self, ax1):
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

    def legend(self, line1, line2, line3):
        num_biked_days = self.stats["num_biked_days"]
        total_miles = self.stats["total_miles"]

        avg_miles = total_miles / self.num_days
        avg_ride_day_miles = total_miles / num_biked_days
        ride_rate = round(num_biked_days / self.num_days * 100, 2)

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

        self.x_axis_days(ax1)
        line1, line2 = self.y_axis_miles(ax1)
        line3 = self.y_axis_percentage(ax1)
        self.legend(line1, line2, line3)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Daily Mileage saved to {self.output_file}.")
