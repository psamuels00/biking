import calendar
import matplotlib
import numpy as np

matplotlib.use("Agg")  # Use a non-interactive backend, prevent icon popping up in Dock on Mac
import matplotlib.pyplot as plt  # noqa E402
import numpy as np  # noqa E402


class Graph:
    def __init__(self, params, stats, output_file, period):
        self.handles = []
        self.labels = []
        self.linspace_params = params.graph.linspace_params
        self.num_biked_days = stats["num_biked_days"]
        self.num_days = stats["num_days"]
        self.output_file = output_file
        self.params = params
        self.period = period
        self.show_only_tracked_days = params.graph.show_only_tracked_days
        self.stats = stats

    def zero2nan(self, data):
        return np.array([n if n is not None and n > 0 else np.nan for n in data])

    def has_31_days(self, date):
        year = date.year
        month = date.month
        num_days = calendar.monthrange(year, month)[1]

        return num_days == 31

    def tick_label(self, date):
        num_days = self.stats["num_days"]

        if date.day == 1:
            label = f"{date.day}\n{date.strftime('%b')}"
        elif date.day == 30:
            if num_days == 30:
                label = "30"
            elif num_days == 60 and self.has_31_days(date):
                label = "30"
            else:
                label = ""
        elif date.day % 5 == 0:
            label = str(date.day)
        else:
            label = ""

        return label

    def get_ticks(self):
        offsets = range(self.num_days)
        labels = [self.tick_label(date) for date in self.stats["data"]["date"]]

        return offsets, labels

    def get_colors(self):
        day_of_week = self.stats["first_day_of_week"]
        num_days = self.stats["num_days"]

        days_of_week = []

        for _ in range(num_days):
            days_of_week.append(day_of_week)
            day_of_week = (day_of_week + 1) % 7

        cm_name = self.params.graph.bar_color_map_name
        shades_of_green = plt.get_cmap(cm_name)(np.linspace(*self.linspace_params, 7))
        colors = [shades_of_green[d] for d in days_of_week]

        return colors

    def title(self, metric):
        plt.title(metric, pad=self.params.graph.title_pad)

    def date_range(self):
        from_date = self.stats["first_date"].strftime("%b %e, %Y")
        to_date = self.stats["last_date"].strftime("%b %e, %Y")

        return from_date, to_date

    def legend(self, loc):
        from_date, to_date = self.date_range()
        plt.legend(
            loc=loc,
            fontsize="small",
            title=f"{from_date} - {to_date}",
            title_fontsize="small",
            handles=self.handles,
            labels=self.labels,
        )

    def no_data_message(self, ax1):
        from_date, to_date = self.date_range()
        message = f"There is no data to plot between\n{from_date} and {to_date}."
        ax1.text(
            0.5,  # X position (relative to axes, where 0 is left and 1 is right)
            0.5,  # Y position (relative to axes, where 0 is bottom and 1 is top)
            message,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
            transform=ax1.transAxes,
            wrap=True,
        )

    def x_axis_values(self):
        values = np.arange(self.num_days)
        num_days = self.params.report.num_days[self.period]
        if num_days is not None:
            values = values[-num_days:]

        return values

    def x_axis_days(self, ax1):
        ax1.set_xlabel("Day")
        tick_offsets, tick_labels = self.get_ticks()
        plt.xticks(tick_offsets, tick_labels, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

    def add_scale(self, ax1, lower_limit, upper_limit, scale):
        if lower_limit != upper_limit:
            ax1.set_ylim(lower_limit, upper_limit)
        ax1.set_yticks(scale, labels=scale, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

        ax2 = ax1.twinx()
        if lower_limit != upper_limit:
            ax2.set_ylim(lower_limit, upper_limit)
        ax2.set_yticks(scale, labels=scale, fontsize="x-small", alpha=self.params.graph.tick_labels_alpha)

    def y_axis(self, ax1):
        pass

    def average_vector(self, values):
        avg_values = []
        sum = 0
        count = 0

        for value in values:
            if value > 0:
                sum += value
                count += 1
            avg_values.append(sum / count if count > 0 else np.nan)

        return avg_values

    def standard_build(self, ax1, title, ylabel, loc="upper left"):
        self.title(title)

        self.x_axis_days(ax1)
        if self.num_biked_days > 0:
            self.y_axis(ax1)
            self.legend(loc)
        else:
            ax1.set_ylabel(ylabel)
            ax1.set_yticks([])
            self.no_data_message(ax1)

    def build(self, ax1):
        pass

    def generate(self):
        fig, ax1 = plt.subplots()
        ax1.set_axisbelow(True)
        self.build(ax1)
        plt.tight_layout()
        plt.savefig(self.output_file, dpi=self.params.graph.dpi, bbox_inches="tight")
        plt.close(fig)
