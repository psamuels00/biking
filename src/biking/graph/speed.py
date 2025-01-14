import math
import numpy as np

from .base import Graph


class SpeedGraph(Graph):
    def build(self, ax1):
        self.title(self.label())

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def label(self):
        return "Speed"

    def scale_step(self):
        return 0.5

    def y_axis(self, ax1):
        self.speed_y_axis(ax1, "speed_per_day", "avg_speed_per_day")

    def speed_y_axis(self, ax1, speed_attr, avg_speed_attr):
        x = np.arange(self.num_days)
        y = self.stats["data"][speed_attr]
        avg_y = self.stats["data"][avg_speed_attr]

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array([n if n > 0 else np.nan for n in avg_y])

        min_value = np.nanmin(nan_y)
        max_value = np.nanmax(nan_y)
        lower_limit = max(0, int(min_value) - 1)
        upper_limit = math.ceil(max_value) + 1
        scale = np.arange(lower_limit, upper_limit, self.scale_step())

        ax1.set_ylabel("Miles/Hour")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale)

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"{self.label()} per Day ({y[-1]:0.1f} mph)")

        line, = ax1.plot(x, avg_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average {self.label()} ({avg_y[-1]:0.1f} mph)")