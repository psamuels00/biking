import os


def attributes(name, **values):
    return type(name, (object,), values)()


class Parameters:
    def __init__(self):
        self.bar_color_map_name = "Greens"
        self.elevation_cache_name = ".cache_open_elevation"
        self.factor_all_days = True  # if False and report_days is N, only factor report days into averages
        self.files = dict(
            distance="Distance.jpg",
            elev_gain="ElevationGain.jpg",
            elev_limits="ElevationLimits.jpg",
            ride_rate="RideRate.jpg",
            performance="Performance.jpg",
            speed="Speed.jpg",
            top_speed="TopSpeed.jpg",
        )
        self.formula = attributes("FormulaParams",
            output_path="output/formula",
            source_path="src/tex",
        )
        self.graph = attributes("GraphParams",
            avg_line_color="tab:blue",
            dpi=300,
            grid_alpha=0.15,
            title_pad=10,
            tick_labels_alpha=0.5,
        )
        self.green_legend_dir = "output/legend"
        self.green_legend_html_file = "green_legend.html"
        self.green_legend_img_file = "green_legend.jpg"
        self.initial_date = "Oct 11, 2024"
        self.journal_file = "data/journal.yaml"
        self.linspace_params = (0.3, 0.9)
        self.obscured_std_start_latlng = (37.96, -121.94)
        self.output_path = "output/graph"
        self.performance = attributes("PerformanceParams",
            d_factor=1.0,
            s_factor=2.0,
            st_factor=0,
            e_factor=3.0,
            er_factor=1.0,
            max_pi_scale=10.0,
        )
        self.report_days = None  # N to limit days reported on, or None for no limit
        self.show_only_tracked_days = True
        self.std_start_elevation_ft = 397
        self.strava = attributes("StravaParams",
            token_url = "https://www.strava.com/oauth/token",
        )
        self.x_ticks_period = 10

    def file(self, name):
        return os.path.join(self.output_path, self.files[name])
