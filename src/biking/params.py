import os
import sys


def attributes(name, **values):
    return type(name, (object,), values)()


def env_load(name):
    value = os.getenv(name)
    if not value:
        print(f"Error: environment variable '{name}' not set or empty.", file=sys.stderr)
        sys.exit(1)

    return value


class Parameters:
    def __init__(self):
        self.elevation_cache_name = ".cache_open_elevation"
        self.formula = attributes("Formula",
            output_path="output/formula",
            source_path="src/tex",
        )
        self.graph = attributes("Graph",
            avg_line_color="tab:blue",
            bar_color_map_name="Greens",
            dpi=300,
            file_names=dict(
                distance="Distance.jpg",
                elev_gain="ElevationGain.jpg",
                elev_limits="ElevationLimits.jpg",
                ride_rate="RideRate.jpg",
                performance="Performance.jpg",
                speed="Speed.jpg",
                top_speed="TopSpeed.jpg",
            ),
            grid_alpha=0.15,
            linspace_params=(0.3, 0.9),
            output_path="output/graph/daily/all",
            show_only_tracked_days=True,
            title_pad=10,
            tick_labels_alpha=0.5,
            x_ticks_period=10,
        )
        self.initial_date = "Oct 11, 2024"
        self.journal_file = "data/journal.yaml"
        self.legend = attributes("Legend",
            dir="output/legend",
            html_file="green_legend.html",
            img_file="green_legend.jpg",
        )
        self.performance = attributes("Performance",
            d_factor=1.0,
            s_factor=2.0,
            st_factor=0,
            e_factor=3.0,
            er_factor=1.0,
            max_pi_scale=10.0,
        )
        self.report = attributes("Report",
            title=dict(
                last30="Last 30 Days",
                last60="Last 60 Days",
                last90="Last 90 Days",
                all="All Time",
            ),

            # N to limit days reported on, or None for no limit
            num_days=dict(
                last30=30,
                last60=60,
                last90=90,
                all=None,
            ),

            # if False and report_days is N, only factor report days into averages
            factor_all_days=dict(
                last30=False,
                last60=False,
                last90=False,
                all=True,
            ),
        )
        self.std_start = attributes("StdStart",
            elevation_ft=397,
            obscured_latlng=(37.96, -121.94),
        )
        self.strava = attributes("Strava",
            auth=attributes("Auth",
                access_tokens_file=".access_tokens",
                client_id=env_load("strava_client_id"),
                client_secret=env_load("strava_client_secret"),
                app_code=env_load("strava_app_auth_code"),
            ),
            http_cache=attributes("HttpCache",
                file=".cache_strava",
                expire_sec=24*3600,
            ),
            url=attributes("Url",
                token="https://www.strava.com/oauth/token",
                athlete="https://www.strava.com/api/v3/athlete",
                activities="https://www.strava.com/api/v3/athlete/activities",
            ),
        )
        self.summary = attributes("Summary",
            output_path = "output/summary/daily",
        )

    def graph_file(self, name):
        return os.path.join(self.graph.output_path, self.graph.file_names[name])
