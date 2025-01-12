from .base import Graph
from collections import namedtuple


Stats = namedtuple("Stats", ["avg", "max", "min", "range"])


def stats(values):
    values = [value for value in values if value > 0]

    average = sum(values) / len(values)
    maximum = max(values)
    minimum = min(values)
    range = maximum - minimum

    return Stats(average, maximum, minimum, range)


class PerformanceGraph(Graph):
    def build(self, ax1):
        self.title("Performance")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = list(range(self.num_days))
        distance_y = self.stats["data"]["distance_per_day"]
        speed_y = self.stats["data"]["avg_speed_per_day"]
        elevation_y = self.stats["data"]["elevation_gain_per_day"]

        distance = stats(distance_y)
        speed = stats(speed_y)
        elevation = stats(elevation_y)

        new_low = 0
        distance_y = [(n - distance.min) / distance.range if n > distance.min else new_low for n in distance_y]
        speed_y = [(n - speed.min) / speed.range if n > speed.min else new_low for n in speed_y]
        elevation_y = [(n - elevation.min) / elevation.range if n > elevation.min else new_low for n in elevation_y]

        d_factor = 1.0
        e_factor = 3.0
        s_factor = 2.0
        global_factor = 10.0
        performance_y = [
            0 if s == 0 else (d * d_factor + e * e_factor + s * s_factor) * global_factor
            for d, s, e in zip(distance_y, speed_y, elevation_y)
        ]

        # def show(label, values):
        #     print(label, ", ".join([f"{value:.1f}" for value in values]))
        #
        # show("DISTANCE", distance_y)
        # show("SPEED", speed_y)
        # show("ELEVATION", elevation_y)
        # show("PERFORMANCE", performance_y)

        ax1.set_ylabel("Performance Index")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        scale = range(0, int(max(performance_y)) + 1, 1)
        self.add_scale(ax1, 0, max(performance_y), scale),

        colors = self.get_colors()
        bar = ax1.bar(x, performance_y, color=colors)
        self.handles.append(bar)
        self.labels.append(f"Performance Index ({performance_y[-1]:0.1f})")