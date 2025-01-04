import matplotlib.pyplot as plt

from .base import Graph


class DistanceGraph(Graph):
    def legend(self, line1, line2):
        num_biked_days = self.stats["num_biked_days"]
        total_miles = self.stats["total_miles"]

        avg_miles = total_miles / self.num_days
        avg_ride_day_miles = total_miles / num_biked_days

        handles = (line1, line2)
        labels = (
            f"Average Distance per Day ({avg_miles:0.1f} mi)",
            f"Average Distance per Ride Day ({avg_ride_day_miles:0.1f} mi)",
        )
        self.set_legend(handles, labels, loc="upper left")

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Distance", pad=30)

        self.x_axis_days(ax1)
        line1, line2 = self.y_axis_distance(ax1)
        self.legend(line1, line2)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
