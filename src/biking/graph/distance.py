from .base import Graph


class DistanceGraph(Graph):
    def build(self, ax1):
        self.title("Distance")

        self.x_axis_days(ax1)
        self.y_axis(ax1)

        self.legend("upper left")

    def y_axis(self, ax1):
        x = list(range(self.num_days))
        y = self.stats["data"]["distance_per_day"]
        avg_y = self.stats["data"]["avg_distance_per_day"]
        avg_ride_day_y = self.stats["data"]["avg_distance_per_ride_day"]

        ax1.set_ylabel("Miles")
        ax1.grid(axis="y", linestyle="-", alpha=0.15)

        scale = range(0, int(max(y)) + 1, 1)
        self.add_scale(ax1, 0, max(y), scale),

        colors = self.get_colors()
        ax1.bar(x, y, color=colors)

        num_biked_days = self.stats["num_biked_days"]
        total_miles = self.stats["total_miles"]

        avg_miles = total_miles / self.num_days
        line, = ax1.plot(x, avg_y, color="lightblue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Distance per Day ({avg_miles:0.1f} mi)")

        avg_ride_day_miles = total_miles / num_biked_days
        line, = ax1.plot(x, avg_ride_day_y, color="tab:blue", marker="o", markersize=3)
        self.handles.append(line)
        self.labels.append(f"Average Distance per Ride Day ({avg_ride_day_miles:0.1f} mi)")