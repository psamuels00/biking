import calendar


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

        data = dict(
            ride_rate_per_day=[],
            daily_mileage_per_day=[],
            avg_daily_mileage_per_day=[],
            avg_ride_day_mileage_per_day=[],
            avg_speed_per_day=[],
            elevation_gain_per_day=[],
        )

        daily_data = self.input_data.get_daily_data()

        for record in daily_data:
            miles = record["distance"]
            num_days += 1
            num_biked_days += (1 if miles else 0)

            if 0 < miles < min_miles:
                min_miles = miles
            max_miles = max(miles, max_miles)
            total_miles += miles

            data["ride_rate_per_day"].append((num_biked_days * 100)/num_days)
            data["daily_mileage_per_day"].append(miles)
            data["avg_daily_mileage_per_day"].append(total_miles/num_days)
            data["avg_ride_day_mileage_per_day"].append(total_miles/num_biked_days)
            data["avg_speed_per_day"].append(record["average_speed"])
            data["elevation_gain_per_day"].append(record["total_elevation_gain"])

        first_date, last_date = self.input_data.date_range
        first_day_of_week = calendar.weekday(first_date.year, first_date.month, first_date.day)

        stats = dict(
            data=data,
            first_date=first_date,
            first_day_of_week=first_day_of_week,
            last_date=last_date,
            max_miles=max_miles,
            min_miles=min_miles,
            num_biked_days=num_biked_days,
            num_days=num_days,
            total_miles=total_miles,
        )

        return stats

    def report(self):
        stats = self.stats
        first_date = stats["first_date"]
        last_date = stats["last_date"]
        max_miles = stats["max_miles"]
        min_miles = stats["min_miles"]
        num_biked_days = stats["num_biked_days"]
        num_days = stats["num_days"]
        total_miles = stats["total_miles"]

        first_day = first_date.strftime("%Y-%m-%d")
        last_day = last_date.strftime("%Y-%m-%d")
        num_skipped_days = num_days - num_biked_days

        ride_rate = round(num_biked_days / num_days * 100, 2)
        avg_miles = total_miles / num_days
        avg_ride_day_miles = total_miles / num_biked_days

        print(f"Date range: {first_day} to {last_day}")
        print()
        print("total days  biked  skipped  ride rate")
        print("----------  -----  -------  ---------")
        print(f"{num_days:10}  {num_biked_days:5}  {num_skipped_days:7}  {ride_rate:8.2f}%")
        print()
        print("biked miles  min   max   avg   avg-per-day-biked")
        print("-----------  ----  ----  ----  -----------------")
        print(f"{total_miles:11.1f}  {min_miles:4.1f}  {max_miles:4.1f}  {avg_miles:4.1f}  {avg_ride_day_miles:17.1f}")
        print()
