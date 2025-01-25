#!/bin/sh

analyze() {
    rm .cache_strava.sqlite
    src/analyze.py > output/console.txt
}

analyze
