import matplotlib.pyplot as plt

from .base import Graph


class ComboGraph(Graph):
    def legend(self, line1, line2, line3):
        num_biked_days = self.stats["num_biked_days"]
        total_miles = self.stats["total_miles"]

        avg_miles = total_miles / self.num_days
        avg_ride_day_miles = total_miles / num_biked_days
        ride_rate = round(num_biked_days / self.num_days * 100, 2)

        plt.legend(
            loc="lower center",
            title="Legend: (latest value in parentheses)",
            title_fontsize="small",
            fontsize="small",
            handles=(line1, line2, line3),
            labels=(
                f"Average Distance per Day ({avg_miles:0.1f} mi)",
                f"Average Distance per Ride Day ({avg_ride_day_miles:0.1f} mi)",
                f"Ride Rate ({ride_rate:5.2f}%)",
            ),
        )

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Combined Metrics", pad=30)

        self.x_axis_days(ax1)
        line1, line2 = self.y_axis_distance(ax1, for_combined_graph=True)
        line3 = self.y_axis_ride_rate(ax1, for_combined_graph=True)
        self.legend(line1, line2, line3)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Combined Metrics saved to {self.output_file}.")
