from .speed import SpeedGraph


class TopSpeedGraph(SpeedGraph):
    def label(self):
        return "Top Speed"

    def y_axis(self, ax1):
        self.speed_y_axis(ax1, "top_speed_per_day", "avg_top_speed_per_day")