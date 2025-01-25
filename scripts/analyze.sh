#!/bin/sh

analyze() {
    rm .cache_strava.sqlite
    (
        echo "<pre>"
        src/analyze.py
        echo "</pre>"
    ) > output/console.html
}

analyze
