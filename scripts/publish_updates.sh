#!/bin/sh

publish() {
    sed 's/\.\.\/\.\.\///' src/pages/graphs/daily.html > docs/index.html
    cp output/graph/* docs/graph/
    (
        echo "<pre>"
        cat output/execution/console.txt
        echo "</pre>"
    ) > docs/console.html

    git add docs
    git commit -m "publish updates"
}

publish
