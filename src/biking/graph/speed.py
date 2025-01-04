from .base import Graph


class SpeedGraph(Graph):
    def build(self, ax1):
        self.title("Speed")

        self.x_axis_days(ax1)
        self.y_axis_speed(ax1)

        self.legend()