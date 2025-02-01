#!/bin/sh

publish() {
    cp -r output/doc/ docs/
    cp src/pages/index.html docs/

    cp -r output/graph/* docs/image/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

    git add docs
    git commit -m "publish updates"
}

publish
