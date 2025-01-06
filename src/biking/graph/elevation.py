from .base import Graph


class ElevationGraph(Graph):
    def build(self, ax1):
        self.title("Elevation")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend("upper left")

    def y_axis(self, ax1):
        x = list(range(self.num_days))
        y_gain = self.stats["data"]["elevation_gain_per_day"]
        y_high = self.stats["data"]["elevation_high_per_day"]
        y_low = self.stats["data"]["elevation_low_per_day"]

        y_gain = [round(n) for n in y_gain]
        y_high = [round(n) for n in y_high]
        y_low = [round(n) for n in y_low]

        ax1.set_ylabel("Feet")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        max_y = int(max(*y_gain, *y_high))
        scale = range(0, max_y + 1, 100)
        self.add_scale(ax1, 0, max_y, scale),

        colors = self.get_colors()
        ax1.bar(x, y_gain, color=colors)

        elevation_gain = self.stats["data"]["elevation_gain_per_day"][-1]
        dots, = ax1.plot(x, y_gain, color="tab:blue", linestyle="None", marker="o", markersize=3)
        self.handles.append(dots)
        self.labels.append(f"Elevation Gain ({elevation_gain:0.1f} ft)")

        elevation_low = self.stats["data"]["elevation_low_per_day"][-1]
        line, = ax1.plot(x, y_low, color="yellow", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation Low ({elevation_low:0.1f} ft)")

        elevation_high = self.stats["data"]["elevation_high_per_day"][-1]
        line, = ax1.plot(x, y_high, color="orange", linestyle="None", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Elevation High ({elevation_high:0.1f} ft)")