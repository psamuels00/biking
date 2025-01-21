#!/bin/sh

./scripts/prep_new_ride.sh $1 && \
./scripts/add_new_ride.sh && \
./scripts/publish_updates.sh && \
git push