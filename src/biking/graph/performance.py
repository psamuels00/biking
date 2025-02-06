import numpy as np

from .base import Graph


def normalize_to_range(values, new_low=0):
    values = [value if value > 0 else np.nan for value in values]

    maximum = np.nanmax(values)
    minimum = np.nanmin(values)

    return [(n - minimum) / (maximum - minimum) if n > minimum else new_low for n in values]


class PerformanceGraph(Graph):
    def build(self, ax1):
        self.title("Performance Index")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def performance_index(self):
        # get metrics as "y" values
        distance_y = self.stats["data"]["distance_per_day"]
        speed_y = self.stats["data"]["speed_per_day"]
        time_y = [d / s if s != 0 else 0 for d, s in zip(distance_y, speed_y)]
        speed_time_y = [s * t for s, t in zip(speed_y, time_y)]
        elevation_y = self.stats["data"]["elevation_gain_per_day"]
        elevation_rate_y = [e / t if t != 0 else 0 for e, t in zip(elevation_y, time_y)]

        # normalize metrics to the range of values for that metric
        distance_y = normalize_to_range(distance_y)
        speed_y = normalize_to_range(speed_y)
        speed_time_y = normalize_to_range(speed_time_y)
        elevation_y = normalize_to_range(elevation_y)
        elevation_rate_y = normalize_to_range(elevation_rate_y)

        d_factor = self.params.performance.d_factor
        s_factor = self.params.performance.s_factor
        st_factor = self.params.performance.st_factor
        e_factor = self.params.performance.e_factor
        er_factor = self.params.performance.er_factor
        max_pi_scale = self.params.performance.max_pi_scale

        # calculate performance index
        performance_y = [
            0 if s == 0 else (d * d_factor + s * s_factor + st * st_factor + e * e_factor + er * er_factor)
            for d, s, st, e, er in zip(distance_y, speed_y, speed_time_y, elevation_y, elevation_rate_y)
        ]

        max_pi = max(performance_y)
        norm_to_scale = lambda values, factor=1: [n * factor / max_pi * max_pi_scale for n in values]

        # normalize performance index and components thereof to the PI scale
        performance_y = norm_to_scale(performance_y)
        d_factor_y = norm_to_scale(distance_y, d_factor)
        s_factor_y = norm_to_scale(speed_y, s_factor)
        st_factor_y = norm_to_scale(speed_time_y, st_factor)
        e_factor_y = norm_to_scale(elevation_y, e_factor)
        er_factor_y = norm_to_scale(elevation_rate_y, er_factor)

        return performance_y, (d_factor_y, s_factor_y, st_factor_y, e_factor_y, er_factor_y)

    def y_axis(self, ax1):
        x = self.x_axis_values()
        y, factors_y = self.performance_index()
        avg_y = self.average_vector(y)
        avg_y = np.array(avg_y)

        nan_y = np.array(y)
        max_value = int(np.nanmax(nan_y))
        lower_limit = 0
        upper_limit = max_value
        scale = range(lower_limit, upper_limit + 1, 1)

        ax1.set_ylabel("Performance Index Unit")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        d_factor_y, s_factor_y, st_factor_y, e_factor_y, er_factor_y = factors_y

        bottom_y = np.array(d_factor_y) + np.array(s_factor_y) + np.array(st_factor_y) + np.array(e_factor_y)
        bar = ax1.bar(x, er_factor_y, bottom=bottom_y, color="crimson")
        self.handles.append(bar)
        self.labels.append(f"Elevation Gain Rate Boost ({er_factor_y[-1]:0.1f})")

        bottom_y = np.array(d_factor_y) + np.array(s_factor_y) + np.array(st_factor_y)
        bar = ax1.bar(x, e_factor_y, bottom=bottom_y, color="orangered")
        self.handles.append(bar)
        self.labels.append(f"Elevation Gain Component ({e_factor_y[-1]:0.1f})")

        if self.params.performance.st_factor > 0:
            bottom_y = np.array(d_factor_y) + np.array(s_factor_y)
            bar = ax1.bar(x, st_factor_y, bottom=bottom_y, color="orange")
            self.handles.append(bar)
            self.labels.append(f"Speed Longevity Boost ({st_factor_y[-1]:0.1f})")

        bottom_y = np.array(d_factor_y)
        bar = ax1.bar(x, s_factor_y, bottom=bottom_y, color="orange")
        self.handles.append(bar)
        self.labels.append(f"Speed Component ({s_factor_y[-1]:0.1f})")

        if self.params.performance.d_factor > 0:
            bar = ax1.bar(x, d_factor_y, color="gold")
            self.handles.append(bar)
            self.labels.append(f"Distance Component ({d_factor_y[-1]:0.1f})")

        avg_color = self.params.graph.avg_line_color
        line, = ax1.plot(x, avg_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Performance Index ({avg_y[-1]:0.1f})")