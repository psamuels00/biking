import matplotlib.pyplot as plt

from .base import Graph


class SpeedGraph(Graph):
    def legend(self, dots1, dots2):
        max_speed = self.stats["data"]["max_speed_per_day"][-1]
        avg_speed = self.stats["data"]["avg_speed_per_day"][-1]

        handles = (dots1, dots2)
        labels = (
            f"Max Speed ({max_speed:0.1f} mph)",
            f"Average Speed ({avg_speed:0.1f} mph)",
        )
        self.set_legend(handles, labels)

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Speed", pad=30)

        self.x_axis_days(ax1)
        dots1, dots2 = self.y_axis_speed(ax1)
        self.legend(dots1, dots2)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
