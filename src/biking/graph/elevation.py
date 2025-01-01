import matplotlib.pyplot as plt

from .base import Graph


class ElevationGraph(Graph):
    def y_axis_elevation(self, ax1):
        y = self.stats["data"]["elevation_gain_per_day"]
        x = list(range(self.num_days))

        y = [round(n) for n in y]

        ax1.set_ylabel("Feet")
        plt.ylim(0, max(y))
        plt.yticks(range(0, int(max(y)) + 1, 100), fontsize="x-small")

        plt.grid(axis="y", linestyle="-", alpha=0.15)

        colors = self.get_colors()
        ax1.bar(x, y, color=colors)
        dots1, = ax1.plot(x, y, color="blue", linestyle="None", marker="o", markersize=3)

        return dots1

    def legend(self, dots1):
        elevation = self.stats["data"]["elevation_gain_per_day"][-1]

        plt.legend(
            loc="lower center",
            title="Legend: (latest value in parentheses)",
            title_fontsize="x-small",
            handles=(dots1,),
            labels=(
                f"Elevation Gain ({elevation:0.1f}ft)",
            ),
        )

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Bike Ride - Daily Elevation Gain", pad=30)

        self.x_axis_days(ax1)
        dots1 = self.y_axis_elevation(ax1)
        self.legend(dots1)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Daily Elevation Gain saved to {self.output_file}.")
