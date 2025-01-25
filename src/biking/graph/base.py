import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, params, stats, output_file, show_only_tracked_days, linspace_params):
        self.stats = stats
        self.num_days = stats["num_days"]
        self.num_biked_days = stats["num_biked_days"]
        self.output_file = output_file
        self.handles = []
        self.labels = []
        self.show_only_tracked_days = show_only_tracked_days
        self.linspace_params = linspace_params
        self.params = params

    def get_ticks(self, period):
        offsets = [0] if self.num_days > 0 else []
        offsets += range(period - 1, self.num_days, period)
        labels = [str(x + 1) for x in offsets]

        return offsets, labels

    def get_colors(self):
        day_of_week = self.stats["first_day_of_week"]
        num_days = self.stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        cm_name = self.params.graph.bar_color_map_name
        shades_of_green = plt.cm.get_cmap(cm_name)(np.linspace(*self.linspace_params, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def title(self, metric):
        plt.title(metric, pad=self.params.graph.title_pad)

    def legend(self, loc="upper left"):
        from_date = self.params.initial_date
        to_date = self.stats["last_date"].strftime("%b %d, %Y")
        plt.legend(
            loc=loc,
            fontsize="small",
            title=f"{from_date} - {to_date}",
            title_fontsize="small",
            handles=self.handles,
            labels=self.labels,
        )

    def x_axis_values(self):
        values = np.arange(self.num_days)
        if self.params.report.num_days is not None:
            values = values[-self.params.report.num_days:]

        return values

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day")
        tick_offsets, tick_labels = self.get_ticks(self.params.graph.x_ticks_period)
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

    def add_scale(self, ax1, lower_limit, upper_limit, scale):
        ax1.set_ylim(lower_limit, upper_limit)
        ax1.set_yticks(scale, labels=scale, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

        ax2 = ax1.twinx()
        ax2.set_ylim(lower_limit, upper_limit)
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

    def build(self, ax1):
        pass

    def generate(self):
        fig, ax1 = plt.subplots()
        self.build(ax1)
        plt.tight_layout()
        plt.savefig(self.output_file, dpi=self.params.graph.dpi, bbox_inches="tight")