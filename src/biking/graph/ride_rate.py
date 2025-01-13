from .base import Graph


class RideRateGraph(Graph):
    def build(self, ax1):
        self.title("Ride Rate")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend("upper right")
        #self.legend("lower center")

    def y_axis(self, ax1):
        x = list(range(self.num_days))
        ride_rate_y = self.stats["data"]["ride_rate_per_day"]

        lower_limit = int(max(0, min(ride_rate_y) // 5 * 5 - 5))
        upper_limit = max(ride_rate_y)
        scale = range(lower_limit, 101, 1)

        ax1.set_ylabel("Percentage")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)
        self.add_scale(ax1, lower_limit, upper_limit, scale),

        ride_rate = ride_rate_y[-1]
        line, = ax1.plot(x, ride_rate_y, marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Ride Rate per Day ({ride_rate:5.2f}%)")