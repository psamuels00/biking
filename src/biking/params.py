import os


class Parameters:
    def __init__(self):
        self.output_path = "output"
        self.files = dict(
            distance="DailyMileage.jpg",
            elevation="DailyElevationGain.jpg",
            speed="DailyAverageSpeed.jpg",
        )

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])

