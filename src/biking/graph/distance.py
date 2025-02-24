import math

from .base import Graph


class DistanceGraph(Graph):
    def build(self, ax1):
        self.standard_build(ax1, "Distance", "Miles")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y = self.stats["data"]["distance_per_day"]
        avg_y = self.stats["data"]["avg_distance_per_day"]

        lower_limit = 0
        upper_limit = math.ceil(max(y))
        scale = range(lower_limit, upper_limit + 1, 1)

        ax1.set_ylabel("Miles")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale)

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Distance per Day ({y[-1]:0.1f} mi)")

        avg_color = self.params.graph.avg_line_color
        (line,) = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Distance ({avg_y[-1]:0.1f} mi)")
