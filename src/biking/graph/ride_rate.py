from .base import Graph


class RideRateGraph(Graph):
    def build(self, ax1):
        self.title("Ride Rate")

        self.x_axis_days(ax1)
        self.y_axis_ride_rate(ax1)

        self.legend()