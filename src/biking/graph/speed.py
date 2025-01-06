from .base import Graph


class SpeedGraph(Graph):
    def build(self, ax1):
        self.title("Speed")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend()

    def y_axis(self, ax1):
        x = list(range(self.num_days))
        y_avg = self.stats["data"]["avg_speed_per_day"]
        y_max = self.stats["data"]["max_speed_per_day"]

        ax1.set_ylabel("Miles/Hour")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        scale = range(0, int(max(y_max)) + 1, 1)
        self.add_scale(ax1, 0, max(y_max), scale),

        colors = self.get_colors(True)
        ax1.vlines(x, ymin=y_avg, ymax=y_max, color=colors, linewidth=3)

        max_speed = self.stats["data"]["max_speed_per_day"][-1]
        dots, = ax1.plot(x, y_max, color="tab:red", linestyle="None", marker="o", markersize=2)
        self.handles.append(dots)
        self.labels.append(f"Max Speed ({max_speed:0.1f} mph)")

        avg_speed = self.stats["data"]["avg_speed_per_day"][-1]
        dots, = ax1.plot(x, y_avg, color="tab:blue", linestyle="None", marker="o", markersize=2)
        self.handles.append(dots)
        self.labels.append(f"Average Speed ({avg_speed:0.1f} mph)")