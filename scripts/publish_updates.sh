#!/bin/sh

publish() {
    rsync -qav --exclude=formula/ --exclude=legend/ output/ docs/
    rsync -qav src/pages/index/index.html docs/

    git add docs
    git commit -m "publish updates"
}

publish
