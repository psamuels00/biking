import numpy as np

from .base import Graph


class PowerGraph(Graph):
    def build(self, ax1):
        self.title("Estimated Power")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y = self.stats["data"]["power_per_day"]
        avg_y = self.stats["data"]["avg_power_per_day"]
        strava_y = self.stats["data"]["strava_estimated_power_per_day"]

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array([n if n > 0 else np.nan for n in avg_y])
        strava_y = np.array([n if n > 0 else np.nan for n in strava_y])

        max_value = int(np.nanmax(nan_y))
        max_value_strava = np.nanmax(strava_y)
        if not np.isnan(max_value_strava):
            max_value = max(max_value, int(max_value_strava))

        min_value = int(np.nanmin(nan_y))
        min_value_strava = np.nanmin(strava_y)
        if not np.isnan(min_value_strava):
            min_value = min(min_value, int(min_value_strava))

        lower_limit = min_value // 5 * 5 - 10
        upper_limit = max_value
        scale = range(lower_limit, upper_limit, 5)

        ax1.set_ylabel("Watts")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Power Output per Day ({y[-1]:0.0f} W)")

        (line,) = ax1.plot(x, strava_y, color="red", linestyle="None", marker="o", markersize=2)
        self.handles.append(line)
        self.labels.append(f"Strava Estimated Power Output ({strava_y[-1]:0.0f} W)")

        avg_color = self.params.graph.avg_line_color
        (line,) = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Power Output ({avg_y[-1]:0.0f} W)")
