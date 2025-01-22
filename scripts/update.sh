#!/bin/sh

./scripts/analyze.sh $1 && \
./scripts/add_bike_ride.sh && \
./scripts/publish_updates.sh && \
git push
