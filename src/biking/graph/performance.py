import numpy as np
from collections import namedtuple

from numpy.ma.extras import compress_nd

from .base import Graph


Stats = namedtuple("Stats", ["avg", "max", "min", "range"])


def stats(values):
    values = [value if value > 0 else np.nan for value in values]

    average = np.nanmean(values)
    maximum = np.nanmax(values)
    minimum = np.nanmin(values)
    range = maximum - minimum

    return Stats(average, maximum, minimum, range)


class PerformanceGraph(Graph):
    def build(self, ax1):
        self.title("Performance")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def performance_index(self):
        distance_y = self.stats["data"]["distance_per_day"]
        speed_y = self.stats["data"]["speed_per_day"]
        elevation_y = self.stats["data"]["elevation_gain_per_day"]

        distance = stats(distance_y)
        speed = stats(speed_y)
        elevation = stats(elevation_y)

        new_low = 0
        distance_y = [(n - distance.min) / distance.range if n > distance.min else new_low for n in distance_y]
        speed_y = [(n - speed.min) / speed.range if n > speed.min else new_low for n in speed_y]
        elevation_y = [(n - elevation.min) / elevation.range if n > elevation.min else new_low for n in elevation_y]

        d_factor = 1.0
        s_factor = 2.0
        e_factor = 3.0
        global_factor = 10.0
        performance_y = [
            0 if s == 0 else (d * d_factor + e * e_factor + s * s_factor) * global_factor
            for d, s, e in zip(distance_y, speed_y, elevation_y)
        ]

        return performance_y

    def avg_performance_index(self, performance_y):
        avg_performance_y = []
        pi_sum = 0
        pi_count = 0

        for pi in performance_y:
            if pi > 0:
                pi_sum += pi
                pi_count += 1
            avg_performance_y.append(pi_sum/pi_count if pi_count > 0 else np.nan)

        return avg_performance_y

    def component(self, ax1, x, component_range, attr_name, color, label, unit):
        y = self.stats["data"][attr_name]
        stats_y = stats(y)
        y = [(n / stats_y.max) * component_range if n > 0 else np.nan for n in y]

        line, = ax1.plot(x, y, color=color, linestyle="None", marker="o", markersize=2)
        self.handles.append(line)
        self.labels.append(f"{label} ({self.stats["data"][attr_name][-1]:0.1f} {unit})")

        avg_y = self.stats["data"]["avg_" + attr_name][-1]
        norm_avg_y = (avg_y / stats_y.max) * component_range
        ax1.axhline(y=norm_avg_y, color=color, linestyle="-", linewidth=0.5)

    def y_axis(self, ax1):
        x = np.arange(self.num_days)
        y = self.performance_index()
        avg_y = self.avg_performance_index(y)

        nan_y = np.array(y)
        if self.show_only_tracked_days:
            pass  # TODO fix this
            # y = nan_y
        avg_y = np.array(avg_y)

        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value + 1
        scale = range(lower_limit, upper_limit, 1)

        ax1.set_ylabel("PI Unit")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        colors = self.get_colors()
        bar = ax1.bar(x, y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Performance Index per Day ({y[-1]:0.1f})")

        line, = ax1.plot(x, avg_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Performance Index ({avg_y[-1]:0.1f})")

        component_range = int(max_value / 2)
        self.component(ax1, x, component_range, "distance_per_day", "gold", "Distance", "mi")
        self.component(ax1, x, component_range, "speed_per_day", "orange", "Speed", "mph")
        self.component(ax1, x, component_range, "elevation_gain_per_day", "orangered", "Elevation Gain", "ft")