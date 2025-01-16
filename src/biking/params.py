import os


class Parameters:
    def __init__(self):
        self.cache_name = ".strava_cache"
        self.files = dict(
            distance="Distance.jpg",
            elevation="Elevation.jpg",
            ride_rate="RideRate.jpg",
            performance="Performance.jpg",
            speed="Speed.jpg",
            top_speed="TopSpeed.jpg",
        )
        self.green_legend_dir = "output/legend"
        self.green_legend_html_file = "green_legend.html"
        self.green_legend_img_file = "green_legend.jpg"
        self.journal_file = "data/journal.json"
        self.obscured_std_start_latlng = (37.96, -121.94)
        self.std_start_elevation_ft = 397
        self.only_tracked_days = True
        self.output_path = "output/graph"
        self.linspace_params = (0.3, 0.9)

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])