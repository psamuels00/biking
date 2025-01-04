import calendar

from .conversions import feet2miles


class Statistics:
    def __init__(self, input_data):
        self.input_data = input_data
        self.stats = self.calculate()

    def calculate(self):
        num_days = 0
        num_biked_days = 0

        max_miles = 0
        min_miles = 999
        total_miles = 0

        max_elev_gain = 0
        min_elev_gain = 999
        total_elev_gain = 0

        max_elev_high = 0
        min_elev_high = 999

        max_elev_low = 0
        min_elev_low = 999

        data = dict(
            ride_rate_per_day=[],
            distance_per_day=[],
            avg_distance_per_day=[],
            avg_distance_per_ride_day=[],
            avg_speed_per_day=[],
            max_speed_per_day=[],
            elevation_gain_per_day=[],
            elevation_high_per_day=[],
            elevation_low_per_day=[],
        )

        daily_data = self.input_data.get_daily_data()

        for record in daily_data:
            miles = record["distance"]
            if 0 < miles < min_miles:
                min_miles = miles
            max_miles = max(miles, max_miles)
            total_miles += miles

            elev_gain = record["total_elevation_gain"]
            if 0 < elev_gain < min_elev_gain:
                min_elev_gain = elev_gain
            max_elev_gain = max(elev_gain, max_elev_gain)
            total_elev_gain += elev_gain

            elev_high = record["elev_high"]
            if 0 < elev_high < min_elev_high:
                min_elev_high = elev_high
            max_elev_high = max(elev_high, max_elev_high)

            elev_low = record["elev_low"]
            if 0 < elev_low < min_elev_low:
                min_elev_low = elev_low
            max_elev_low = max(elev_low, max_elev_low)

            num_days += 1
            num_biked_days += (1 if miles else 0)

            data["ride_rate_per_day"].append((num_biked_days * 100)/num_days)
            data["distance_per_day"].append(miles)
            data["avg_distance_per_day"].append(total_miles/num_days)
            data["avg_distance_per_ride_day"].append(total_miles/num_biked_days)
            data["avg_speed_per_day"].append(record["average_speed"])
            data["max_speed_per_day"].append(record["max_speed"])
            data["elevation_gain_per_day"].append(elev_gain)
            data["elevation_high_per_day"].append(elev_high)
            data["elevation_low_per_day"].append(elev_low)

        first_date, last_date = self.input_data.date_range
        first_day_of_week = calendar.weekday(first_date.year, first_date.month, first_date.day)

        stats = dict(
            data=data,
            first_date=first_date,
            first_day_of_week=first_day_of_week,
            last_date=last_date,
            max_elev_gain=max_elev_gain,
            max_elev_high=max_elev_high,
            max_elev_low=max_elev_low,
            max_miles=max_miles,
            min_elev_gain=min_elev_gain,
            min_elev_high=min_elev_high,
            min_elev_low=min_elev_low,
            min_miles=min_miles,
            num_biked_days=num_biked_days,
            num_days=num_days,
            total_elev_gain=total_elev_gain,
            total_miles=total_miles,
        )

        return stats

    def report(self):
        stats = self.stats
        data = stats["data"]

        first_date = stats["first_date"]
        last_date = stats["last_date"]
        max_elev_gain = int(stats["max_elev_gain"])
        max_elev_high = int(stats["max_elev_high"])
        max_elev_low = int(stats["max_elev_low"])
        max_miles = stats["max_miles"]
        max_speed_avg = max(data["avg_speed_per_day"])
        max_speed_max = max(data["max_speed_per_day"])
        min_elev_gain = int(stats["min_elev_gain"])
        min_elev_high = int(stats["min_elev_high"])
        min_elev_low = int(stats["min_elev_low"])
        min_miles = stats["min_miles"]
        min_speed_avg = min(x for x in data["avg_speed_per_day"] if x > 0)
        min_speed_max = min(x for x in data["max_speed_per_day"] if x > 0)
        num_biked_days = stats["num_biked_days"]
        num_days = stats["num_days"]
        total_elev_gain = int(stats["total_elev_gain"])
        total_elev_gain_miles = feet2miles(total_elev_gain)
        total_miles = stats["total_miles"]

        first_day = first_date.strftime("%Y-%m-%d")
        last_day = last_date.strftime("%Y-%m-%d")
        num_skipped_days = num_days - num_biked_days

        ride_rate = round(num_biked_days / num_days * 100, 2)
        avg_miles = total_miles / num_days
        avg_ride_day_miles = total_miles / num_biked_days

        print(f"Date range: {first_day} to {last_day}")
        print()
        print("days  total  biked  skipped  ride rate")
        print("      -----  -----  -------  ---------")
        print(f"{num_days:11}  {num_biked_days:5}  {num_skipped_days:7}  {ride_rate:8.2f}%")
        print()
        print("distance (miles)  min   max   avg   avg-per-day-biked  total")
        print("                  ----  ----  ----  -----------------  -------")
        print(f"{min_miles:22.1f}  {max_miles:4.1f}  {avg_miles:4.1f}  {avg_ride_day_miles:17.1f}  {total_miles:7.1f}")
        print()
        print("elevation gain (ft)  min   max   total    total miles")
        print("                     ----  ----  -------  -----------")
        print(f"{min_elev_gain:25}  {max_elev_gain:4}  {total_elev_gain:7}  {total_elev_gain_miles:11.1f}")
        print()
        print("elevation range (ft)  low:  min   max   high:  min   max")
        print("                            ----  ----         ----  ----")
        print(f"{min_elev_low:31}  {max_elev_low:4}  {min_elev_high:12}  {max_elev_high:4}")
        print()
        print("speed (mph)  avg:  min   max   max:  min   max")
        print("                   ----  ----        ----  ----")
        print(f"{min_speed_avg:23.1f}  {max_speed_avg:4.1f}  {min_speed_max:10.1f}  {max_speed_max:4.1f}")
