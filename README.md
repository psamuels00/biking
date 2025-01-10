# Biking Statistics

Generate graphs such as the following from data collected using Strava.

![Daily Bike Ride - Distance](output/Distance.jpg)
![Daily Bike Ride - Ride Rate](output/RideRate.jpg)
![Daily Bike Ride - Speed](output/Speed.jpg)
![Daily Bike Ride - Elevation Gain](output/Elevation.jpg)

There is also a way to augment the Strava data.  See <a href="#input">Input</a> below.


## Create a Strava app

Follow [Getting Started with the Strava API](https://developers.strava.com/docs/getting-started/)
to create a Strava app.


### Get an Initial Access Code:

Go to [this URL](http://www.strava.com/oauth/authorize?client_id=999999&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,activity:read).
Replace 999999 with your client_id and submit the form..
Finally, parse the app auth code from the redirect URL:

    http://localhost/exchange_token?state=&code=4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c&scope=read,read_all


### Define Strava Access Variables

Define the following environment variables:

    strava_client_id=999999
    strava_client_secret=8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f
    strava_app_auth_code=4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c


## Installation

    pip install -r requirements


## Execution

    src/analyze.py

To update the data after a ride:

    ./scripts/prep_new_route.sh <#miles>
    ./scripts/add_new_route.sh

eg:

    ./scripts/prep_new_route.sh 15 && ./scripts/add_new_route.sh


## Input
<a name="input"></a>

*TODO*


## Output

Output looks like this:

    Date range: 2024-10-11 to 2025-01-09

    days  total  biked  skipped  ride rate
          -----  -----  -------  ---------
             91     82        9     90.11%

    distance (miles)  min   max   avg   avg-per-day-biked  total
                      ----  ----  ----  -----------------  -------
                       6.9  31.4  13.4               14.8   1216.6

    elevation gain (ft)  min   max   total    total miles
                         ----  ----  -------  -----------
                           11  2031    37132          7.0

    elevation range (ft)  low:  min   max   high:  min   max
                                ----  ----         ----  ----
                                 17   256           390  1009

    speed (mph)  avg:  min   max   max:  min   max
                       ----  ----        ----  ----
                        9.1  14.5        22.9  38.7
    DISTANCE 3.5, 2.5, 3.1, 3.8, 3.8, 3.8, 4.4, 4.7, 7.6, 2.8, 3.5, 3.5, 3.5, 3.8, 0.3, 4.7, 3.1, 2.5, 5.4, 3.5, 4.4, 5.1, 3.5, 0.3, 5.4, 3.8, 4.4, 5.7, 4.1, 5.8, 5.8, 0.3, 4.4, 3.5, 0.3, 8.2, 3.0, 2.5, 4.9, 5.7, 4.2, 0.3, 3.8, 7.5, 3.8, 0.3, 4.2, 7.5, 5.3, 5.6, 5.1, 6.0, 5.0, 8.0, 5.8, 3.8, 4.9, 10.3, 4.5, 4.4, 6.9, 5.2, 5.6, 5.8, 4.9, 5.2, 0.3, 8.5, 7.8, 4.8, 0.3, 7.2, 3.6, 5.3, 6.4, 3.8, 3.8, 5.8, 8.1, 3.5, 6.7, 6.8, 5.8, 4.0, 8.4, 2.7, 6.3, 4.0, 3.4, 0.3, 6.6
    SPEED -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, -2.8, 3.5, 4.0, -2.8, 3.5, -2.8, -2.8, 5.0, 3.8, 4.9, 4.7, 4.9, 4.6, -2.8, 4.6, 5.1, -2.8, -2.8, 5.0, 7.2, 4.4, 3.8, 4.7, 5.5, 4.8, 6.5, 4.6, 5.5, 5.5, 5.2, 4.8, 5.3, 4.3, 4.2, 5.2, 5.3, 4.9, 4.7, -2.8, 5.3, 5.4, 4.8, -2.8, 5.8, 5.0, 4.8, 4.1, 4.7, 5.4, 5.5, 5.9, 6.7, 5.7, 5.2, 4.2, -2.8, 5.3, 4.4, 5.2, 5.1, 5.6, -2.8, 5.8
    ELEVATION 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 6.5, 4.0, 1.5, 6.6, 1.5, 1.5, 5.6, 3.5, 3.9, 4.9, 4.9, 3.2, 1.5, 4.6, 4.0, 1.5, 1.5, 4.8, 1.5, 4.9, 6.1, 5.4, 3.5, 6.3, 4.7, 9.6, 4.6, 5.5, 7.8, 4.4, 4.5, 9.0, 8.1, 4.7, 3.5, 4.7, 4.6, 1.5, 4.6, 3.6, 3.8, 1.5, 4.0, 3.0, 5.2, 11.5, 4.5, 4.6, 5.6, 5.0, 3.7, 5.6, 5.8, 4.7, 1.5, 6.4, 2.9, 4.6, 3.4, 3.1, 1.5, 4.6
    PERFORMANCE 2.1, 1.1, 1.8, 2.4, 2.4, 2.4, 3.1, 3.4, 6.3, 1.5, 2.1, 2.1, 2.1, 2.4, -1.1, 3.4, 1.8, 1.2, 4.0, 2.1, 3.1, 3.7, 2.1, -1.1, 4.0, 2.4, 3.1, 4.3, 2.7, 15.7, 13.7, -1.1, 14.4, 2.1, -1.1, 18.8, 10.3, 11.4, 14.5, 15.6, 12.0, -1.1, 13.0, 16.5, 2.4, -1.1, 14.0, 16.3, 14.6, 15.5, 15.2, 15.0, 16.1, 19.2, 20.0, 13.9, 15.9, 23.3, 13.7, 14.2, 20.2, 17.5, 15.5, 14.6, 14.4, 14.5, -1.1, 18.4, 16.8, 13.4, -1.1, 17.0, 11.6, 15.4, 22.0, 13.1, 13.8, 16.9, 19.0, 13.9, 18.0, 17.8, 14.7, 2.7, 20.1, 10.0, 16.0, 12.6, 12.0, -1.1, 16.9
