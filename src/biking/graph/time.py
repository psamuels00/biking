import math
import numpy as np

from .base import Graph


class TimeGraph(Graph):
    def build(self, ax1):
        self.standard_build(ax1, "Time", "Minutes")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y = self.stats["data"]["time_per_day"]
        avg_y = self.stats["data"]["avg_time_per_day"]

        nan_y = self.zero2nan(y)
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = self.zero2nan(avg_y)

        min_value = np.nanmin(nan_y)
        max_value = np.nanmax(nan_y)
        lower_limit = int(min_value // 5 * 5 - 10)
        upper_limit = int(max_value)
        scale = range(lower_limit, upper_limit, 5)

        ax1.set_ylabel("Minutes")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale)

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Time per Day ({y[-1]:0.1f} min)")

        avg_color = self.params.graph.avg_line_color
        (line,) = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Time ({avg_y[-1]:0.1f} min)")
