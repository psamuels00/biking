import numpy as np

from .base import Graph


class WorkGraph(Graph):
    def build(self, ax1):
        self.standard_build(ax1, "Estimated Work", "kilojoule")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y = self.stats["data"]["work_per_day"]
        avg_y = self.stats["data"]["avg_work_per_day"]

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array([n if n > 0 else np.nan for n in avg_y])

        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit, 50)

        ax1.set_ylabel("kilojoule")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Work per Day ({y[-1]:0.0f} kJ)")

        avg_color = self.params.graph.avg_line_color
        (line,) = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Work ({avg_y[-1]:0.0f} kJ)")
