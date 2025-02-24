import numpy as np

from .base import Graph


class ElevationLimitsGraph(Graph):
    def build(self, ax1):
        self.standard_build(ax1, "Elevation Limits", "Feet")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y_low = self.stats["data"]["elevation_low_per_day"]
        y_high = self.stats["data"]["elevation_high_per_day"]
        y_start = self.stats["data"]["elevation_start_per_day"]

        nan_y_low = self.zero2nan(y_low)
        nan_y_high = self.zero2nan(y_high)
        nan_y_start = self.zero2nan(y_start)

        if self.show_only_tracked_days:
            y_low = nan_y_low
            y_high = nan_y_high
            y_start = nan_y_start
            max_value = int(np.nanmax(np.concatenate((nan_y_high, nan_y_start))))
        else:
            max_value = int(max(*y_high, *(x for x in y_start if x is not None)))

        last_low_value = nan_y_low[np.isfinite(nan_y_low)][-1]
        last_high_value = nan_y_high[np.isfinite(nan_y_high)][-1]
        last_start_value = nan_y_start[np.isfinite(nan_y_start)][-1]

        # ensure the graph aligns with others since there is no average plot to provide non-nan data
        if self.show_only_tracked_days and np.isnan(y_low[-1]):
            y_low[-1] = 0
            y_high[-1] = 0

        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit + 100, 100)

        ax1.set_ylabel("Feet")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        linewidth = 8 if self.num_days <= 30 else 4
        vlines = ax1.vlines(x, ymin=y_low, ymax=y_high, colors=colors, linewidth=linewidth)
        self.handles.append(vlines)
        self.labels.append(f"Elevation Range ({last_low_value:0.0f} - {last_high_value:0.0f} ft)")

        (line,) = ax1.plot(x, y_start, color="red", linestyle="None", marker="o", markersize=2)
        self.handles.append(line)
        self.labels.append(f"Elevation Start ({last_start_value:.0f} ft)")
