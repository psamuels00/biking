#!/bin/sh

publish() {
    cp src/pages/graphs/daily/all.html docs/index.html
    cp src/pages/graphs/daily/last*.html docs/

    cp -r output/graph/* docs/graph/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

#    git add docs
#    git commit -m "publish updates"
}

publish
