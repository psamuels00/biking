#!/bin/sh

publish() {
    cp -r output/doc/ docs/
    cp src/pages/index.html docs/

    cp -r output/graph/* docs/graph/

    mkdir -p docs/summary
    cp -r output/summary/* docs/summary/

    if [ "$1" != "dev" ]; then
        git add docs
        git commit -m "publish updates"
    fi
}

publish $1
