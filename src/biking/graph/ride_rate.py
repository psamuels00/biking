import matplotlib.pyplot as plt

from .base import Graph


class RideRateGraph(Graph):
    def legend(self, line1):
        num_biked_days = self.stats["num_biked_days"]
        ride_rate = round(num_biked_days / self.num_days * 100, 2)

        plt.legend(
            loc="lower center",
            title="Legend: (latest value in parentheses)",
            title_fontsize="small",
            fontsize="small",
            handles=(line1,),
            labels=(
                f"Ride Rate ({ride_rate:5.2f}%)",
            ),
        )

    def generate(self):
        fig, ax1 = plt.subplots()
        plt.title("Daily Bike Ride - Ride Rate", pad=30)

        self.x_axis_days(ax1)
        line1 = self.y_axis_ride_rate(ax1)
        self.legend(line1)

        plt.tight_layout()

        plt.savefig(self.output_file, dpi=300, bbox_inches="tight")
        print(f"Ride Rate saved to {self.output_file}.")
