import matplotlib.pyplot as plt

from .base import Graph


class ElevationGraph(Graph):
    def legend(self, dots1):
        elevation = self.stats["data"]["elevation_gain_per_day"][-1]

        handles = (dots1, )
        labels = (
            f"Elevation Gain ({elevation:0.1f}ft)",
        )
        self.set_legend(handles, labels)

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Elevation", pad=30)

        self.x_axis_days(ax1)
        dots1 = self.y_axis_elevation(ax1)
        self.legend(dots1)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Elevation graph saved to {self.output_file}.")
