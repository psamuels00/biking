# Biking Statistics

Generate a graph such as the following from a list of (day, miles) pairs:

![Daily Mileage and Ride Rate Combined into a Single Graph](output/DailyMileage.jpg)


## Installation

    pip install -r requirements


## Execution

    src/show_stats.py


## Input

The input consists of a list of (day, miles) pairs, encoded in the names of files, which should look like this:

    images/bike-route-20241011-10mi.png
    images/bike-route-20241012-07mi.png
    images/bike-route-20241013-09mi.png
    ...

For the purpose of this program, the content of the files is irrelevant.

## Output

Output looks like this:

    Date range: 2024-10-11 to 2024-11-30

    total days  biked  skipped  % biked
    ----------  -----  -------  -------
            51     45        6      88%

    biked miles  min  max   avg   avg-per-day-biked
    -----------  ---  ---  -----  -----------------
            589    7   25   11.5               13.1

    Daily Mileage per Day saved to DailyMileage.jpg.

An example of the generated graph is shown above.
