#!/bin/sh

analyze() {
    rm .cache_strava.sqlite
    src/analyze.py
}

analyze
