import numpy as np
from collections import namedtuple

from .base import Graph


def stats(values):
    values = [value if value > 0 else np.nan for value in values]

    maximum = np.nanmax(values)
    minimum = np.nanmin(values)
    range = maximum - minimum

    Stats = namedtuple("Stats", ["min", "range"])
    return Stats(minimum, range)


class PerformanceGraph(Graph):
    def build(self, ax1):
        self.title("Performance Index")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def performance_index(self):
        distance_y = self.stats["data"]["distance_per_day"]
        speed_y = self.stats["data"]["speed_per_day"]
        time_y = [d / s if s != 0 else 0 for d, s in zip(distance_y, speed_y)]
        speed_time_y = [s * t for s, t in zip(speed_y, time_y)]
        elevation_y = self.stats["data"]["elevation_gain_per_day"]
        elevation_rate_y = [e / t if t != 0 else 0 for e, t in zip(elevation_y, time_y)]

        d_factor = 1.0
        s_factor = 2.0
        st_factor = 0
        e_factor = 3.0
        er_factor = 1.0
        max_pi_scale = 10.0

        distance = stats(distance_y)
        speed = stats(speed_y)
        speed_time = stats(speed_time_y)
        elevation = stats(elevation_y)
        elevation_rate = stats(elevation_rate_y)

        new_low = 0
        distance_y = [(n - distance.min) / distance.range if n > distance.min else new_low for n in distance_y]
        speed_y = [(n - speed.min) / speed.range if n > speed.min else new_low for n in speed_y]
        speed_time_y = [(n - speed_time.min) / speed_time.range if n > speed_time.min else new_low for n in speed_time_y]
        elevation_y = [(n - elevation.min) / elevation.range if n > elevation.min else new_low for n in elevation_y]
        elevation_rate_y = [(n - elevation_rate.min) / elevation_rate.range if n > elevation_rate.min else new_low for n in elevation_rate_y]

        performance_y = [
            0 if s == 0 else (d * d_factor + s * s_factor + st * st_factor + e * e_factor + er * er_factor)
            for d, s, st, e, er in zip(distance_y, speed_y, speed_time_y, elevation_y, elevation_rate_y)
        ]

        max_pi = max(performance_y)
        performance_y = [n / max_pi * max_pi_scale for n in performance_y]

        d_factor_y = [d * d_factor / max_pi * max_pi_scale for d in distance_y]
        s_factor_y = [s * s_factor / max_pi * max_pi_scale for s in speed_y]
        st_factor_y = [st * st_factor / max_pi * max_pi_scale for st in speed_time_y]
        e_factor_y = [e * e_factor / max_pi * max_pi_scale for e in elevation_y]
        er_factor_y = [er * er_factor / max_pi * max_pi_scale for er in elevation_rate_y]

        return performance_y, (d_factor_y, s_factor_y, st_factor_y, e_factor_y, er_factor_y)

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

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y, factors_y = self.performance_index()
        avg_y = self.avg_performance_index(y)

        nan_y = np.array(y)
        if self.show_only_tracked_days:
            y = nan_y
        avg_y = np.array(avg_y)

        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit + 1, 1)

        ax1.set_ylabel("Performance Index Unit")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        d_factor_y, s_factor_y, st_factor_y, e_factor_y, er_factor_y = factors_y

        bottom_y = np.zeros_like(d_factor_y)

        bar = ax1.bar(x, d_factor_y, color="#e59866")
        self.handles.append(bar)
        self.labels.append(f"Distance Component ({d_factor_y[-1]:0.1f})")
        bottom_y += np.array(d_factor_y)

        bar = ax1.bar(x, s_factor_y, bottom=bottom_y, color="#f7dc6f")
        self.handles.append(bar)
        self.labels.append(f"Speed Component ({s_factor_y[-1]:0.1f})")
        bottom_y += np.array(s_factor_y)

        bar = ax1.bar(x, st_factor_y, bottom=bottom_y, color="#f1c40f")
        self.handles.append(bar)
        self.labels.append(f"Speed Longevity Boost ({st_factor_y[-1]:0.1f})")
        bottom_y += np.array(st_factor_y)

        bar = ax1.bar(x, e_factor_y, bottom=bottom_y, color="#f5b7b1")
        self.handles.append(bar)
        self.labels.append(f"Elevation Gain Component ({e_factor_y[-1]:0.1f})")
        bottom_y += np.array(e_factor_y)

        bar = ax1.bar(x, er_factor_y, bottom=bottom_y, color="#f1948a")
        self.handles.append(bar)
        self.labels.append(f"Elevation Gain Rate Boost ({er_factor_y[-1]:0.1f})")

        line, = ax1.plot(x, avg_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Performance Index ({avg_y[-1]:0.1f})")