#!/bin/sh

analyze() {
    rm .cache_strava.sqlite
    local mark='Output looks like this:'
    (
        sed "/$mark/q" README.md
        echo
        src/analyze.py | sed '/./s/^/    /'
    ) > TMP.md
    mv TMP.md README.md
}

analyze
