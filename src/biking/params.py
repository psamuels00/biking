import os


class Parameters:
    def __init__(self):
        self.output_path = "output"
        self.files = dict(
            combo="CombinedMetrics.jpg",
            distance="Distance.jpg",
            elevation="Elevation.jpg",
            ride_rate="RideRate.jpg",
            speed="Speed.jpg",
        )

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])

