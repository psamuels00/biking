import numpy as np

from .base import Graph


class ElevationGraph(Graph):
    def build(self, ax1):
        self.title("Elevation")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = np.arange(self.num_days)
        y = self.stats["data"]["elevation_gain_per_day"]
        avg_y = self.stats["data"]["avg_elevation_gain_per_day"]

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array([n if n > 0 else np.nan for n in avg_y])

        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value + 100
        scale = range(lower_limit, upper_limit, 100)

        ax1.set_ylabel("Feet")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Elevation Gain per Day ({y[-1]:0.1f} mi)")

        line, = ax1.plot(x, avg_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Elevation Gain ({avg_y[-1]:0.1f} mph)")

        y_low = self.stats["data"]["elevation_low_per_day"]
        y_high = self.stats["data"]["elevation_high_per_day"]

        y_low = np.array([n if n > 0 else np.nan for n in y_low])
        y_high = np.array([n if n > 0 else np.nan for n in y_high])

        line, = ax1.plot(x, y_low, color="yellow", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation Low ({y_low[-1]:0.1f} ft)")

        line, = ax1.plot(x, y_high, color="orange", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation High ({y_high[-1]:0.1f} ft)")