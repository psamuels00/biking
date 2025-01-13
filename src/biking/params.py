import os


class Parameters:
    def __init__(self):
        self.output_path = "output"
        self.files = dict(
            distance="Distance.jpg",
            elevation="Elevation.jpg",
            ride_rate="RideRate.jpg",
            performance="Performance.jpg",
            speed="Speed.jpg",
            top_speed="TopSpeed.jpg",
        )
        self.only_tracked_days = False

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])

