import numpy as np

from biking.power import output_power
from .power import PowerGraph


class EnergyGraph(PowerGraph):
    def build(self, ax1):
        self.title("Estimated Energy")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = self.x_axis_values()
        elev_y = self.stats["data"]["elevation_gain_per_day"]
        speed_y = self.stats["data"]["speed_per_day"]
        dist_y = self.stats["data"]["distance_per_day"]

        y = self.calculate_output_power(1, elev_y, speed_y, dist_y)
        avg_y = self.average_vector(y)

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y

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
        self.labels.append(f"Energy per Day ({y[-1]:0.0f} kJ)")

        avg_color = self.params.graph.avg_line_color
        line, = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Energy ({avg_y[-1]:0.0f} kJ)")
