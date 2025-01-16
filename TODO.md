# TODO

### High Priority
- Add configuration parameters:
  - report_days = number of days to limit graph to, eg: 30 to show the most recent 30 days
  - factor_all_days = True to include all days in calculation of averages, False to include only the report days
- Ensure no overlap in X-axis tick labels
- Make sure everything works when there are no Strava activities
- Filter biking activities from all returned by Strava

### Medium Priority
- Add date labels somehow instead of day number, for example:

      | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
          1 Dec   5        10        15        20        25        30   1 Jan   5

- Completely separate configuration from the code
- Do something better than the hack to convert starting location
- Add support for multiple activities per day
- Simplify input: maybe add activities manually via Strava, or at least make it easier to enter data manually

### Low Priority
- Add Weekly, Monthly, and Yearly rollup graphs
- Make the graphs interactive!?
- Add a spreadsheet, IDE, and AI chat!!? _(just kidding)_
