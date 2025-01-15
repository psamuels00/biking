import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, stats, output_file, only_tracked_days, linspace_params):
        self.stats = stats
        self.num_days = stats["num_days"]
        self.num_biked_days = stats["num_biked_days"]
        self.output_file = output_file
        self.handles = []
        self.labels = []
        self.show_only_tracked_days = only_tracked_days
        self.linspace_params = linspace_params

    def get_ticks(self, period):
        offsets = [0] + [x - 1 for x in range(period, self.num_days, period)]
        if self.num_days % period != 1:
            offsets += [self.num_days - 1]
        labels = [str(x + 1) for x in offsets]

        return offsets, labels

    def get_colors(self):
        day_of_week = self.stats["first_day_of_week"]
        num_days = self.stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        shades_of_green = plt.cm.Greens(np.linspace(*self.linspace_params, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def title(self, metric):
        title = f"Bike Ride - Daily {metric}"
        plt.title(title, pad=5)

    def legend(self, loc="upper left"):
        from_date = "Oct 11, 2024"
        to_date = self.stats["last_date"].strftime("%b %d, %Y")
        plt.legend(
            loc=loc,
            fontsize="small",
            title=f"{from_date} - {to_date}",
            title_fontsize="small",
            handles=self.handles,
            labels=self.labels,
        )

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day")
        tick_offsets, tick_labels = self.get_ticks(period=5)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small", alpha=0.5)

    def add_scale(self, ax1, lower_limit, upper_limit, scale):
        ax1.set_ylim(lower_limit, upper_limit)
        ax1.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.5)

        ax2 = ax1.twinx()
        ax2.set_ylim(lower_limit, upper_limit)
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=0.5)

    def build(self, ax1):
        pass

    def generate(self):
        fig, ax1 = plt.subplots()
        self.build(ax1)
        plt.tight_layout()
        plt.savefig(self.output_file, dpi=300, bbox_inches="tight")