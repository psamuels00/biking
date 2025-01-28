#!/bin/sh

publish() {
    cp src/pages/graphs/daily/*.html docs/
    cp src/pages/graphs/daily/last30.html docs/index.html

    cp -r output/graph/* docs/graph/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

#    git add docs
#    git commit -m "publish updates"
}

publish
