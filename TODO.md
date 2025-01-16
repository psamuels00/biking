# TODO

### High Priority
- Make sure everything works when there are no Strava activities and activities other than biking
- Add configuration parameters:
  - report_days = number of days to limit graph to, eg: 30 to show the most recent 30 days
  - factor_all_days = True to include all days in calculation of averages, False to include only the report days
- Ensure no overlap in X-axis tick labels

### Medium Priority
- Completely separate configuration from the code
- Add support for multiple activities per day
- Add date labels somehow instead of day number, for example:

      | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
          1 Dec   5        10        15        20        25        30   1 Jan   5

### Low Priority
- Add Weekly, Monthly, and Yearly rollup graphs
- Make the graphs interactive!?
- Add a spreadsheet, IDE, and AI chat!!? _(just kidding)_