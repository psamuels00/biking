import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime


class Graph:
    def __init__(self, stats, output_file):
        self.stats = stats
        self.num_days = stats["num_days"]
        self.output_file = output_file
        self.handles = []
        self.labels = []

    def get_ticks(self, period):
        offsets = [0] + [x - 1 for x in range(period, self.num_days, period)]
        if self.num_days % period != 1:
            offsets += [self.num_days - 1]
        labels = [str(x + 1) for x in offsets]

        return offsets, labels

    def get_colors(self, light=False):
        day_of_week = self.stats["first_day_of_week"]
        num_days = self.stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        linspace_params = (0.2, 0.5) if light else (0.3, 0.9)
        shades_of_green = plt.cm.Greens(np.linspace(*linspace_params, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def title(self, metric):
        from_date = "Oct 11, 2024"
        to_date = datetime.now().strftime("%b %d, %Y")
        title = "\n".join([
            f"Daily Bike Ride - {metric}",
            f"{from_date} - {to_date}",
        ])

        plt.title(title, pad=30)

    def legend(self, loc="lower center"):
        plt.legend(
            loc=loc,
            fontsize="small",
            title="Legend: (latest value in parentheses)",
            title_fontsize="small",
            handles=self.handles,
            labels=self.labels,
        )

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day")
        tick_offsets, tick_labels = self.get_ticks(period=5)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small")

    def add_scale(self, ax1, lower_limit, upper_limit, scale):
        ax1.set_ylim(lower_limit, upper_limit)
        ax1.set_yticks(scale, labels=scale, fontsize="x-small")

        ax2 = ax1.twinx()
        ax2.set_ylim(lower_limit, upper_limit)
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.25)

    def build(self, ax1):
        pass

    def generate(self):
        fig, ax1 = plt.subplots()
        self.build(ax1)
        plt.tight_layout()
        plt.savefig(self.output_file, dpi=300, bbox_inches="tight")