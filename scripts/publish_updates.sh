#!/bin/sh

publish() {
    cp -r output/index/ docs/index/
    cp src/pages/index/index.html docs/

    cp -r output/graph/* docs/image/

    cp -r output/inputs/ docs/inputs/
    cp -r output/metrics/ docs/metrics/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

    git add docs
    git commit -m "publish updates"
}

publish
