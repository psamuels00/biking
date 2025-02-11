# TODO

### High Priority
- Save all the data pulled from Strava in a database or file, not only in HTTP requests cache, in case Strava
  suddenly makes older data inaccessible.  Also, be smarter about paging through the activities; paging is
  probably not necessary if I'm caching values.

### Medium Priority
- Implement Input.details() as CSV or HTML
- Implement Statistics.details() and Statistics.summary() as CSV or HTML
- Add Weekly, Monthly, and Yearly rollup graphs.

### Low Priority
- Generate green_legend.jpg automatically somehow
- Maybe save graph legends separately from the graphs??
