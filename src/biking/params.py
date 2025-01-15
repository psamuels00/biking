import os


class Parameters:
    def __init__(self):
        self.output_path = "output/graph"
        self.files = dict(
            distance="Distance.jpg",
            elevation="Elevation.jpg",
            ride_rate="RideRate.jpg",
            performance="Performance.jpg",
            speed="Speed.jpg",
            top_speed="TopSpeed.jpg",
        )
        self.only_tracked_days = True
        self.linspace_params = (0.3, 0.9)
        self.green_legend_dir = "output/legend"
        self.green_legend_html_file = "green_legend.html"
        self.green_legend_img_file = "green_legend.jpg"

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])