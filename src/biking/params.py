import os


def attributes(name, **values):
    return type(name, (object,), values)()


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
            output_path="output/graph",
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
            num_days=None,  # N to limit days reported on, or None for no limit
            factor_all_days=True,  # if False and report_days is N, only factor report days into averages
        )
        self.std_start = attributes("StdStart",
            elevation_ft=397,
            obscured_latlng=(37.96, -121.94),
        )

    def graph_file(self, name):
        return os.path.join(self.graph.output_path, self.graph.file_names[name])
