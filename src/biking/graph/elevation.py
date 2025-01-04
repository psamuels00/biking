import matplotlib.pyplot as plt

from .base import Graph


class ElevationGraph(Graph):
    def legend(self, dots1, line1, line2):
        elevation_gain = self.stats["data"]["elevation_gain_per_day"][-1]
        elevation_low = self.stats["data"]["elevation_low_per_day"][-1]
        elevation_high = self.stats["data"]["elevation_high_per_day"][-1]

        handles = (dots1, line1, line2)
        labels = (
            f"Elevation Gain ({elevation_gain:0.1f} ft)",
            f"Elevation Low ({elevation_low:0.1f} ft)",
            f"Elevation High ({elevation_high:0.1f} ft)",
        )
        self.set_legend(handles, labels, loc="upper left")

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Elevation", pad=30)

        self.x_axis_days(ax1)
        dots1, line1, line2 = self.y_axis_elevation(ax1)
        self.legend(dots1, line1, line2)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
