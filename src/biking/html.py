from dotmap import DotMap

from biking.conversions import period2days
from biking.format import format_input_record, format_metrics_record
from biking.template import render


class Renderer:
    def render_page(self, params, page_params, data, output_file):
        template_root = params.html.template_root
        template_path = page_params.template_path
        template_file = page_params.template_file
        output_path = page_params.output_path

        render(template_root, template_path, template_file, data, output_path, output_file)


class PeriodHtml(Renderer):
    def __init__(self, params, period):
        self.params = params
        self.period = period

    def page_params(self):
        return DotMap()  # override

    def get_rows(self, num):
        return []  # override

    def format_record(self, rec):
        return {}  # override

    def render(self, rows):
        page_params = self.page_params()
        data = dict(period=self.period, rows=rows)
        output_file = f"{self.period}.html"
        self.render_page(self.params, page_params, data, output_file)

    def generate_page(self):
        num = period2days(self.period)
        rows = self.get_rows(num)
        rows = [self.format_record(rec) for rec in rows]
        self.render(rows)


class IndexHtml(PeriodHtml):
    def page_params(self):
        return self.params.html.index


class InputsDetailsHtml(PeriodHtml):
    def __init__(self, params, period, input_data):
        super().__init__(params, period)
        self.input_data = input_data

    def page_params(self):
        return self.params.html.inputs.details

    def get_rows(self, num):
        return self.input_data.get_daily_data(num)

    def format_record(self, rec):
        return format_input_record(rec)


class MetricsDetailsHtml(PeriodHtml):
    def __init__(self, params, period, statistics):
        super().__init__(params, period)
        self.statistics = statistics

    def page_params(self):
        return self.params.html.metrics.details

    def get_rows(self, num):
        return self.statistics.metrics_data(num)

    def format_record(self, rec):
        return format_metrics_record(rec)


class MetricsSummaryHtml(Renderer):
    def __init__(self, params, summary_info):
        self.params = params
        self.summary_info = summary_info

    def page_params(self):
        return self.params.html.metrics.summary

    def render(self, summary_info):
        page_params = self.page_params()
        data = dict(data=summary_info)
        output_file = "daily.html"
        self.render_page(self.params, page_params, data, output_file)

    def generate_page(self):
        self.render(self.summary_info)
