#!/bin/sh

analyze() {
    rm .strava_cache.sqlite
    local mark='Output looks like this:'
    (
        sed "/$mark/q" README.md
        echo
        src/analyze.py | sed '/./s/^/    /'
    ) > TMP.md
    mv TMP.md README.md
}

analyze
