#!/bin/sh

prep_new_ride() {
    if [ -n "$1" ]; then
        ./scripts/prep_new_ride.sh $1
    fi
}

prep_new_ride "$1" && \
./scripts/analyze.sh && \
./scripts/add_bike_ride.sh && \
./scripts/publish_updates.sh && \
git push
