#!/bin/sh

publish() {
    sed 's/\.\.\/\.\.\///' output/doc/graphs/daily.html > docs/index.html
    cp output/graph/* docs/graph/
    cp output/console.html docs/

    git add docs
    git commit -m "publish updates"
}

publish
