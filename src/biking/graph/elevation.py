import matplotlib.pyplot as plt

from .base import Graph


class ElevationGraph(Graph):
    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Elevation", pad=30)

        self.x_axis_days(ax1)
        self.y_axis_elevation(ax1)
        self.legend("upper left")

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
