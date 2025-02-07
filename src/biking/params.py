import os
import sys

from dotmap import DotMap


def env_load(name):
    value = os.getenv(name)
    if not value:
        print(f"Error: environment variable '{name}' not set or empty.", file=sys.stderr)
        sys.exit(1)

    return value


class Parameters():
    def __init__(self):
        data = dict(
            calories=dict(
                min_work_efficiency=0.20,
                max_work_efficiency=0.25,
            ),
            elevation_cache_name=".cache_open_elevation",
            formula=dict(
                output_path="output/formula",
                source_path="src/tex",
            ),
            graph=dict(
                avg_line_color="tab:blue",
                alt_line_color="tab:purple",
                bar_color_map_name="Greens",
                dpi=300,
                file_names=dict(
                    calories="Calories.jpg",
                    distance="Distance.jpg",
                    elev_gain="ElevationGain.jpg",
                    elev_limits="ElevationLimits.jpg",
                    energy="Energy.jpg",
                    ride_rate="RideRate.jpg",
                    performance="Performance.jpg",
                    power="Power.jpg",
                    speed="Speed.jpg",
                    top_speed="TopSpeed.jpg",
                ),
                grid_alpha=0.15,
                linspace_params=(0.3, 0.9),
                output_path="output/graph/daily",
                show_only_tracked_days=True,
                title_pad=10,
                tick_labels_alpha=0.5,
            ),
            html=dict(
                template_path="src/pages",
                template_file="daily.html",
                output_path="output/doc/daily",
            ),
            journal_file="data/journal.yaml",
            legend=dict(
                dir="output/legend",
                html_file="green_legend.html",
                img_file="green_legend.jpg",
            ),
            performance=dict(
                d_factor=1.0,
                s_factor=2.0,
                st_factor=0,
                e_factor=3.0,
                er_factor=1.0,
                max_pi_scale=10.0,
            ),
            power=dict(
                constants=dict(
                    g=9.81,  # Acceleration due to gravity (m/s^2)
                    C_d=0.88,  # Drag coefficient for a cyclist
                    A=0.5,  # Frontal area in m^2
                ),
                cyclist_weight_lbs=150,
                cyclist_accessories_oz=dict(  # the keys are irrelevant, only the values are used, summed
                    knapsack_w_inner_tube_and_tools=36,
                    clothes=32,
                    helmet=16,
                    iPhone_Xs=6.24,
                    gloves=1.76,

                ),
                bike_weight_lbs=31.11,  # Trek Marlin 6 second gen, factory weight
                bike_accessories_oz=dict(  # the keys are irrelevant, only the values are used, summed
                    u_lock=35.27,
                    tire_liner=19.4,
                    seat=18.7,
                    mudguards=17.63,
                    handlebar_ends=5.4,
                    front_light=3.5,
                    power_grips=1.76,
                    rear_lights=1,
                ),
            ),
            report=dict(
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
            ),
            std_start=dict(
                elevation_ft=397,
                obscured_latlng=(37.96, -121.94),
            ),
            strava=dict(
                auth=dict(
                    access_tokens_file=".access_tokens",
                    client_id=env_load("strava_client_id"),
                    client_secret=env_load("strava_client_secret"),
                    app_code=env_load("strava_app_auth_code"),
                ),
                http_cache=dict(
                    file=".cache_strava",
                    expire_sec=24*3600,
                ),
                url=dict(
                    token="https://www.strava.com/oauth/token",
                    athlete="https://www.strava.com/api/v3/athlete",
                    activities="https://www.strava.com/api/v3/athlete/activities",
                ),
            ),
            summary=dict(
                output_path="output/summary/daily",
            ),
        )
        self._data = DotMap(data)

    def __getattr__(self, item):
        return self._data[item]

    def graph_file(self, period, name):
        return os.path.join(self.graph.output_path, period, self.graph.file_names[name])
