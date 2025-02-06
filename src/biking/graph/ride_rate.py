from .base import Graph


class RideRateGraph(Graph):
    def build(self, ax1):
        self.title("Ride Rate")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend("upper right")

    def y_axis(self, ax1):
        x = self.x_axis_values()
        ride_rate_y = self.stats["data"]["ride_rate_per_day"]

        min_ride_rate = min(ride_rate_y)
        if min_ride_rate >= 80:
            step = 1
        elif min_ride_rate >= 60:
            step = 2
        else:
            step = 5
        upper_limit = 100
        lower_limit = int(max(0, min_ride_rate - step) // step * step)
        scale = range(lower_limit, 101, step)

        ax1.set_ylabel("Percentage")
        ax1.grid(axis="y", linestyle="-", alpha=self.params.graph.grid_alpha)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        avg_color = self.params.graph.avg_line_color
        line, = ax1.plot(x, ride_rate_y, color=avg_color, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Ride Rate per Day ({ride_rate_y[-1]:5.2f}%)")
