import matplotlib.pyplot as plt

from .base import Graph


class ComboGraph(Graph):
    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Combined Metrics", pad=30)

        self.x_axis_days(ax1)
        self.y_axis_distance(ax1, for_combined_graph=True)
        self.y_axis_ride_rate(ax1, for_combined_graph=True)
        self.legend()

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
