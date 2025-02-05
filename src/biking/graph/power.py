import numpy as np

from .base import Graph
from biking.power import output_power


class PowerGraph(Graph):
    def build(self, ax1):
        self.title("Power Estimate")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def get_weight_params(self):
        power = self.params.power

        cyclist_accessories_oz = 0
        for _, weight_oz in power.cyclist_accessories_oz.items():
            cyclist_accessories_oz += weight_oz
        cyclist_weight = power.cyclist_weight_lbs + cyclist_accessories_oz / 16

        bike_accessories_oz = 0
        for _, weight_oz in power.bike_accessories_oz.items():
            bike_accessories_oz += weight_oz
        bike_weight = power.bike_weight_lbs + bike_accessories_oz / 16

        return cyclist_weight, bike_weight

    def y_axis(self, ax1):
        x = self.x_axis_values()
        elev_y = self.stats["data"]["elevation_gain_per_day"]
        speed_y = self.stats["data"]["speed_per_day"]
        dist_y = self.stats["data"]["distance_per_day"]

        cyclist_weight, bike_weight = self.get_weight_params()

        y = [output_power(cyclist_weight, bike_weight, elevation_gain, speed, distance)[0] if speed else 0
             for elevation_gain, speed, distance in zip(elev_y, speed_y, dist_y)]
        avg_y = [n/2 for n in y]

        nan_y = np.array([n if n > 0 else np.nan for n in y])
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array([n if n > 0 else np.nan for n in avg_y])

        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit, 10)

        ax1.set_ylabel("Watts")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Power Output per Day ({y[-1]:0.0f} W)")

        avg_color = self.params.graph.avg_line_color
        line, = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Power Output ({avg_y[-1]:0.0f} ft)")
