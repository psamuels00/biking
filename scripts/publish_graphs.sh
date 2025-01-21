#!/bin/sh

publish() {
    sed 's/\.\.\/\.\.\///' output/doc/graphs/daily.html > docs/index.html
    cp output/graph/* docs/graph/

    git add docs
    git commit -m "publish update"
    git push
}

publish
