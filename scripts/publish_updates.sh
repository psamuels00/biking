#!/bin/sh

publish() {
    cp output/doc/*.html docs/
    cp output/doc/last30.html docs/index.html

    cp -r output/graph/* docs/graph/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

    git add docs
    git commit -m "publish updates"
}

publish
