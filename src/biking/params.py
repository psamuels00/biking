import os


class Parameters:
    def __init__(self):
        self.output_path = "output"
        self.files = dict(
            mileage="DailyMileage.jpg",
            elevation_gain="DailyElevationGain.jpg",
            avg_speed="DailyAvgSpeed.jpg",
        )

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])

