import matplotlib.pyplot as plt

from .base import Graph


class SpeedGraph(Graph):
    def y_axis_speed(self, ax1):
        y_avg = self.stats["data"]["avg_speed_per_day"]
        y_max = self.stats["data"]["max_speed_per_day"]
        x = list(range(self.num_days))

        # remove_zeroes = False
        # if remove_zeroes:
        #     x = []
        #     y_avg = []
        #     y_max = []
        #     y = zip(
        #         self.stats["data"]["avg_speed_per_day"],
        #         self.stats["data"]["max_speed_per_day"],
        #     )
        #     for n, (avg_value, max_value) in enumerate(y):
        #         if avg_value and max_value:
        #             x.append(n)
        #             y_avg.append(avg_value)
        #             y_max.append(max_value)

        ax1.set_ylabel("Miles/Hour")
        plt.ylim(0, max(y_max))
        plt.yticks(range(0, int(max(y_max)) + 1, 1), fontsize="x-small")

        plt.grid(axis="y", linestyle="-", alpha=0.15)

        colors = self.get_colors(True)
        ax1.vlines(x, ymin=y_avg, ymax=y_max, color=colors, linewidth=3)#, alpha=0.25)
        dots1, = ax1.plot(x, y_max, color="red", linestyle="None", marker="o", markersize=2)
        dots2, = ax1.plot(x, y_avg, color="blue", linestyle="None", marker="o", markersize=2)

        return dots1, dots2

    def legend(self, dots1, dots2):
        max_speed = self.stats["data"]["max_speed_per_day"][-1]
        avg_speed = self.stats["data"]["avg_speed_per_day"][-1]

        plt.legend(
            loc="lower center",
            title="Legend: (latest value in parentheses)",
            title_fontsize="x-small",
            handles=(dots1, dots2),
            labels=(
                f"Max Speed ({max_speed:0.1f})",
                f"Average Speed ({avg_speed:0.1f})",
            ),
        )

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Bike Ride - Daily Average Speed", pad=30)

        self.x_axis_days(ax1)
        dots1, dots2 = self.y_axis_speed(ax1)
        self.legend(dots1, dots2)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300)
        print(f"Daily Average Speed saved to {self.output_file}.")
