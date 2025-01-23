#!/bin/sh

prep_new_ride() {
    if [ -n "$1" ]; then
        echo ./scripts/prep_new_ride.sh $1
    fi
}

prep_new_ride "$1" && \
echo ./scripts/analyze.sh && \
echo ./scripts/add_bike_ride.sh && \
echo ./scripts/publish_updates.sh && \
echo git push
