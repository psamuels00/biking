from dotmap import DotMap

from biking.conversions import period2days
from biking.template import render


class Html:
    def __init__(self, params, period):
        self.params = params
        self.period = period

    def format_numeric(self, value, prec=0, empty=""):
        return empty if not value else f"{value:.{prec}f}"

    def page_params(self):
        return DotMap()  # override

    def get_rows(self, num):
        return []  # override

    def format_row(self, row):
        return {}  # override

    def render(self, rows):
        page_params = self.page_params()
        template_path = page_params.template_path
        template_file = page_params.template_file
        output_path = page_params.output_path
        output_file = f"{self.period}.html"

        data = dict(period=self.period, rows=rows)
        render(template_path, template_file, data, output_path, output_file)

    def generate_page(self):
        num = period2days(self.period)
        rows = self.get_rows(num)
        rows = [self.format_row(row) for row in rows]
        self.render(rows)


class IndexHtml(Html):
    def page_params(self):
        return self.params.html.index


class InputsHtml(Html):
    def __init__(self, params, period, input_data):
        super().__init__(params, period)
        self.input_data = input_data

    def page_params(self):
        return self.params.html.inputs.details

    def get_rows(self, num):
        return self.input_data.get_daily_data(num)

    def format_row(self, row):
        return dict(
            ymd=row["ymd"],
            date=row["date"],
            distance=self.format_numeric(row["distance"], 1),
            average_speed=self.format_numeric(row["average_speed"], 1),
            top_speed=self.format_numeric(row["top_speed"], 1),
            total_elevation_gain=self.format_numeric(row["total_elevation_gain"]),
            elev_high=self.format_numeric(row["elev_high"]),
            elev_low=self.format_numeric(row["elev_low"]),
            elev_start=self.format_numeric(row["elev_start"]),
            power=self.format_numeric(row["power"]),
        )


class MetricsHtml(Html):
    def __init__(self, params, period, statistics):
        super().__init__(params, period)
        self.statistics = statistics

    def page_params(self):
        return self.params.html.metrics.details

    def get_rows(self, num):
        return self.statistics.metrics_data(num)

    def format_row(self, row):
        (
            date,
            distance,
            avg_distance,
            speed,
            avg_speed,
            top_speed,
            avg_top_speed,
            elevation,
            avg_elevation,
            power,
            avg_power,
            energy,
            avg_energy,
            calories,
            avg_calories,
            ride_rate,
        ) = row

        return dict(
            date=date,
            distance=self.format_numeric(distance, 1),
            avg_distance=self.format_numeric(avg_distance, 1),
            speed=self.format_numeric(speed, 1),
            avg_speed=self.format_numeric(avg_speed, 1),
            top_speed=self.format_numeric(top_speed, 1),
            avg_top_speed=self.format_numeric(avg_top_speed, 1),
            elevation=self.format_numeric(elevation),
            avg_elevation=self.format_numeric(avg_elevation),
            power=self.format_numeric(power),
            avg_power=self.format_numeric(avg_power),
            energy=self.format_numeric(energy),
            avg_energy=self.format_numeric(avg_energy),
            calories=self.format_numeric(calories),
            avg_calories=self.format_numeric(avg_calories),
            ride_rate=self.format_numeric(ride_rate, 2),
        )
