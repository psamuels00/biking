import numpy as np

from .base import Graph


class ElevationLimitsGraph(Graph):
    def build(self, ax1):
        self.title("Elevation Limits")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y_low = self.stats["data"]["elevation_low_per_day"]
        y_high = self.stats["data"]["elevation_high_per_day"]
        y_start = self.stats["data"]["elevation_start_per_day"]

        if self.show_only_tracked_days:
            y_low = np.array([n if n > 0 else np.nan for n in y_low])
            y_high = np.array([n if n > 0 else np.nan for n in y_high])
            y_start = np.array([np.nan if n is None else n for n in y_start])
            max_value = int(np.nanmax(np.concatenate((y_high, y_start))))
        else:
            max_value = int(max(*y_high, *(x for x in y_start if x is not None)))

        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit + 100, 100)

        ax1.set_ylabel("Feet")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        vlines = ax1.vlines(x, ymin=y_low, ymax=y_high, colors=colors, linewidth=4)
        self.handles.append(vlines)
        self.labels.append(f"Elevation Range ({y_low[-1]:0.0f} - {y_high[-1]:0.0f} ft)")

        line, = ax1.plot(x, y_start, color="red", linestyle="None", marker="o", markersize=2)
        self.handles.append(line)
        self.labels.append(f"Elevation Start ({y_start[-1]:.0f} ft)")
