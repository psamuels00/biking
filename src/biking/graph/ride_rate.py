import matplotlib.pyplot as plt

from .base import Graph


class RideRateGraph(Graph):
    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Ride Rate", pad=30)

        self.x_axis_days(ax1)
        self.y_axis_ride_rate(ax1)
        self.legend()

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300, bbox_inches="tight")
