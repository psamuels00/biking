def format_numeric(value, empty, limit_precision, precision=0):
    return empty if not value else f"{value:.{precision}f}" if limit_precision else value


def format_input_record(rec, empty="", limit_precision=True):
    return dict(
        ymd=rec["ymd"],
        date=rec["date"],
        distance=format_numeric(rec["distance"], empty, limit_precision, 1),
        average_speed=format_numeric(rec["average_speed"], empty, limit_precision, 1),
        top_speed=format_numeric(rec["top_speed"], empty, limit_precision, 1),
        total_elevation_gain=format_numeric(rec["total_elevation_gain"], empty, limit_precision),
        elev_high=format_numeric(rec["elev_high"], empty, limit_precision),
        elev_low=format_numeric(rec["elev_low"], empty, limit_precision),
        elev_start=format_numeric(rec["elev_start"], empty, limit_precision),
        power=format_numeric(rec["power"], empty, limit_precision),
    )


def format_metrics_record(rec, empty="", limit_precision=True):
    return dict(
        date=rec["date"],
        distance=format_numeric(rec["distance"], empty, limit_precision, 1),
        avg_distance=format_numeric(rec["avg_distance"], empty, limit_precision, 1),
        speed=format_numeric(rec["speed"], empty, limit_precision, 1),
        avg_speed=format_numeric(rec["avg_speed"], empty, limit_precision, 1),
        top_speed=format_numeric(rec["top_speed"], empty, limit_precision, 1),
        avg_top_speed=format_numeric(rec["avg_top_speed"], empty, limit_precision, 1),
        elevation=format_numeric(rec["elevation"], empty, limit_precision),
        avg_elevation=format_numeric(rec["avg_elevation"], empty, limit_precision),
        power=format_numeric(rec["power"], empty, limit_precision),
        avg_power=format_numeric(rec["avg_power"], empty, limit_precision),
        energy=format_numeric(rec["energy"], empty, limit_precision),
        avg_energy=format_numeric(rec["avg_energy"], empty, limit_precision),
        calories=format_numeric(rec["calories"], empty, limit_precision),
        avg_calories=format_numeric(rec["avg_calories"], empty, limit_precision),
        ride_rate=format_numeric(rec["ride_rate"], empty, limit_precision, 2),
    )
