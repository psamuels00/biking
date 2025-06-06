import math
import numpy as np

from .base import Graph


class CaloriesGraph(Graph):
    def build(self, ax1):
        self.standard_build(ax1, "Estimated Total Caloric Burn", "Calories")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y = self.stats["data"]["calories_per_day"]

        min_e = self.params.calories.min_work_efficiency
        max_e = self.params.calories.max_work_efficiency
        lower_y = [n / max_e for n in y]
        upper_y = [n / min_e for n in y]
        mean_y = [n / ((min_e + max_e) / 2) for n in y]
        avg_y = self.average_vector(mean_y)

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        nan_lower_y = np.array([n if n > 0 else np.nan for n in lower_y])
        nan_upper_y = np.array([n if n > 0 else np.nan for n in upper_y])
        if self.show_only_tracked_days:
            y = nan_y
            lower_y = nan_lower_y
            upper_y = nan_upper_y

        max_value = int(np.nanmax(nan_upper_y))
        lower_limit = 0
        upper_limit = math.ceil(max_value / 100) * 100
        scale = range(lower_limit, upper_limit + 1, 50)

        ax1.set_ylabel("Calories")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, bottom=lower_y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Calories per Day ({lower_y[-1]:0.0f}-{upper_y[-1]:0.0f} kCal)")

        avg_color = self.params.graph.avg_line_color
        (line,) = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Calories ({avg_y[-1]:0.0f} kCal)")
